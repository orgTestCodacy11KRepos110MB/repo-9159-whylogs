"""
TODO:
    * Implement histograms
"""
import datasketches
import pandas as pd

from whylabs.logs.core.statistics.datatypes import (
    FloatTracker,
    IntTracker,
    VarianceTracker,
)
from whylabs.logs.core.statistics.thetasketch import ThetaSketch
from whylabs.logs.core.summaryconverters import (
    histogram_from_sketch,
    quantiles_from_sketch,
)
from whylabs.logs.proto import NumbersMessage, NumberSummary
from whylabs.logs.util import dsketch, stats

# Parameter controlling histogram accuracy.  Larger = more accurate
DEFAULT_HIST_K = 256


class NumberTracker:
    """
    Class to track statistics for numeric data.

    Parameters
    ----------
    variance
        Tracker to follow the variance
    floats
        Float tracker for tracking all floats
    ints
        Integer tracker

    Attributes
    ----------
    variance
        See above
    floats
        See above
    ints
        See above
    theta_sketch : `whylabs.logs.core.statistics.thetasketch.ThetaSketch`
        Sketch which tracks approximate cardinality
    """

    def __init__(
        self,
        variance: VarianceTracker = None,
        floats: FloatTracker = None,
        ints: IntTracker = None,
        theta_sketch: ThetaSketch = None,
        histogram: datasketches.kll_floats_sketch = None,
        frequent_numbers: dsketch.FrequentNumbersSketch = None,
    ):
        # Our own trackers
        if variance is None:
            variance = VarianceTracker()
        if floats is None:
            floats = FloatTracker()
        if ints is None:
            ints = IntTracker()
        if theta_sketch is None:
            theta_sketch = ThetaSketch()
        if histogram is None:
            histogram = datasketches.kll_floats_sketch(DEFAULT_HIST_K)
        if frequent_numbers is None:
            frequent_numbers = dsketch.FrequentNumbersSketch()
        self.variance = variance
        self.floats = floats
        self.ints = ints
        self.theta_sketch = theta_sketch
        self.histogram = histogram
        self.frequent_numbers = frequent_numbers

    @property
    def count(self):
        return self.variance.count

    def track(self, number):
        """
        Add a number to statistics tracking

        Parameters
        ----------
        number : int, float
            A numeric value
        """
        if pd.isnull(number):
            return
        self.variance.update(number)
        self.theta_sketch.update(number)
        self.frequent_numbers.update(number)
        # TODO: histogram update
        # Update floats/ints counting
        f_value = float(number)
        self.histogram.update(f_value)
        if self.floats.count > 0:
            self.floats.update(f_value)
        # Note: this type checking is fragile in python.  May want to include
        # numpy.integer in the type check
        elif isinstance(number, int):
            self.ints.update(number)
        else:
            self.floats.add_integers(self.ints)
            self.ints.set_defaults()
            self.floats.update(f_value)

    def merge(self, other):
        # Make a copy of the histogram
        hist_copy = datasketches.kll_floats_sketch.deserialize(
            self.histogram.serialize()
        )
        hist_copy.merge(other.histogram)

        theta_sketch = self.theta_sketch.merge(other.theta_sketch)
        frequent_numbers = self.frequent_numbers.merge(other.frequent_numbers)
        return NumberTracker(
            variance=self.variance.merge(other.variance),
            floats=self.floats.merge(other.floats),
            ints=self.ints.merge(other.ints),
            theta_sketch=theta_sketch,
            histogram=hist_copy,
            frequent_numbers=frequent_numbers,
        )

    def to_protobuf(self):
        """
        Return the object serialized as a protobuf message
        """
        opts = dict(
            variance=self.variance.to_protobuf(),
            compact_theta=self.theta_sketch.serialize(),
            histogram=self.histogram.serialize(),
            frequent_numbers=self.frequent_numbers.to_protobuf(),
        )
        if self.floats.count > 0:
            opts["doubles"] = self.floats.to_protobuf()
        elif self.ints.count > 0:
            opts["longs"] = self.ints.to_protobuf()
        msg = NumbersMessage(**opts)
        return msg

    @staticmethod
    def from_protobuf(message: NumbersMessage):
        """
        Load from a protobuf message

        Returns
        -------
        number_tracker : NumberTracker
        """
        theta = None
        if message.theta is not None and len(message.theta) > 0:
            theta = ThetaSketch.deserialize(message.theta)
        elif message.compact_theta is not None and len(message.compact_theta) > 0:
            theta = ThetaSketch.deserialize(message.compact_theta)

        opts = dict(
            theta_sketch=theta,
            variance=VarianceTracker.from_protobuf(message.variance),
            histogram=dsketch.deserialize_kll_floats_sketch(message.histogram),
            frequent_numbers=dsketch.FrequentNumbersSketch.from_protobuf(
                message.frequent_numbers
            ),
        )
        if message.HasField("doubles"):
            opts["floats"] = FloatTracker.from_protobuf(message.doubles)
        if message.HasField("longs"):
            opts["ints"] = IntTracker.from_protobuf(message.longs)
        return NumberTracker(**opts)

    def to_summary(self):
        """
        Construct a `NumberSummary` message

        Returns
        -------
        summary : NumberSummary
            Summary of the tracker statistics
        """
        if self.variance.count == 0:
            return

        stddev = self.variance.stddev()
        doubles = self.floats.to_protobuf()
        if doubles.count > 0:
            mean = self.floats.mean()
            min = doubles.min
            max = doubles.max
        else:
            mean = self.ints.mean()
            min = float(self.ints.min)
            max = float(self.ints.max)

        unique_count = self.theta_sketch.to_summary()
        histogram = histogram_from_sketch(self.histogram)
        quant = quantiles_from_sketch(self.histogram)
        frequent_numbers = self.frequent_numbers.to_summary()
        num_records = self.variance.count
        cardinality = unique_count.estimate
        discrete = stats.is_discrete(num_records, cardinality)

        return NumberSummary(
            count=self.variance.count,
            stddev=stddev,
            min=min,
            max=max,
            mean=mean,
            histogram=histogram,
            quantiles=quant,
            unique_count=unique_count,
            frequent_numbers=frequent_numbers,
            is_discrete=discrete,
        )
