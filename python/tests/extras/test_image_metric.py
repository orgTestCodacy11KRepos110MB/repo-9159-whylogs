import logging
import os
from typing import Dict

import whylogs as why
from whylogs.api.writer.whylabs import _uncompund_dataset_profile
from whylogs.core.configs import SummaryConfig
from whylogs.core.datatypes import DataType
from whylogs.core.metrics import (
    DistributionMetric,
    FrequentItemsMetric,
    Metric,
    MetricConfig,
)
from whylogs.core.preprocessing import ListView, PreprocessedColumn
from whylogs.core.resolvers import Resolver
from whylogs.core.schema import ColumnSchema, DatasetSchema
from whylogs.extras.image_metric import ImageMetric, ImageMetricConfig, log_image

logger = logging.getLogger(__name__)

try:
    from PIL.Image import Image as ImageType
except ImportError as e:
    ImageType = None
    logger.debug(str(e))
    logger.debug("Unable to load PIL; install Pillow for image support")


TEST_DATA_PATH = os.path.abspath(
    os.path.join(
        os.path.realpath(os.path.dirname(__file__)),
        os.pardir,
        "testdata",
    )
)


def image_loader(path: str = None) -> ImageType:
    from PIL import Image  # to throw if PIL's not available

    with open(path, "rb") as file_p:
        img = Image.open(file_p).copy()
        return img


IMAGE_METRIC_CONFIG = ImageMetricConfig(
    exif_tags={
        "ImageWidth": DistributionMetric.zero(MetricConfig()),
        "PhotometricInterpretation": DistributionMetric.zero(MetricConfig()),
        "Orientation": DistributionMetric.zero(MetricConfig()),
        "ResolutionUnit": DistributionMetric.zero(MetricConfig()),
        "Software": FrequentItemsMetric.zero(MetricConfig()),
    }
)


class TestResolver(Resolver):
    def resolve(self, name: str, why_type: DataType, column_schema: ColumnSchema) -> Dict[str, Metric]:
        return {ImageMetric.get_namespace(IMAGE_METRIC_CONFIG): ImageMetric.zero(IMAGE_METRIC_CONFIG)}


def test_image_metric() -> None:
    image_path = os.path.join(TEST_DATA_PATH, "images", "flower2.jpg")
    img = image_loader(image_path)
    ppc = PreprocessedColumn()
    ppc.list = ListView(objs=[img])
    metric = ImageMetric.zero(IMAGE_METRIC_CONFIG)
    metric.columnar_update(ppc)
    summary = metric.to_summary_dict(SummaryConfig())
    assert summary["image/ImagePixelWidth/mean"] > 0
    assert summary["image/ImageWidth/max"] == 1733
    assert summary["image/PhotometricInterpretation/min"] == 2
    assert summary["image/Orientation/max"] == 1
    assert summary["image/ResolutionUnit/max"] == 2
    assert "image/Software/frequent_strings" in summary


def test_log_image() -> None:
    image_path = os.path.join(TEST_DATA_PATH, "images", "flower2.jpg")
    img = image_loader(image_path)
    results = log_image([img], config=IMAGE_METRIC_CONFIG).view()
    logger.info(results.get_column("image_0").to_summary_dict())
    assert results.get_column("image_0").to_summary_dict()["image/image/ImagePixelWidth/mean"] > 0
    assert results.get_column("image_0").to_summary_dict()["image/image/Orientation/max"] == 1


def test_log_interface() -> None:
    image_path = os.path.join(TEST_DATA_PATH, "images", "flower2.jpg")
    img = image_loader(image_path)

    schema = DatasetSchema(resolvers=TestResolver())

    results = why.log(row={"image_col": img}, schema=schema).view().get_column("image_col")
    logger.info(results.to_summary_dict())
    assert results.to_summary_dict()["image/image/ImagePixelWidth/mean"] > 0


def test_uncompound_profile() -> None:
    image_path = os.path.join(TEST_DATA_PATH, "images", "flower2.jpg")
    img = image_loader(image_path)
    profile_view = log_image(img, "image_column").view()
    uncompounded = _uncompund_dataset_profile(profile_view)
    assert "image_column" in uncompounded._columns
    assert "image" in uncompounded._columns["image_column"]._metrics  # original compound metric
    assert "image_column.image.ImagePixelWidth" in uncompounded._columns
    assert "distribution" in uncompounded._columns["image_column.image.ImagePixelWidth"]._metrics  # uncompounded
