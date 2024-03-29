from unittest.mock import MagicMock, Mock

import pytest

from whylogs.core import ColumnProfileView, DatasetProfileView
from whylogs.viz.utils.descriptive_stats import (
    _calculate_descriptive_statistics,
    _get_count_metrics_from_column_view,
    _get_dist_metrics_from_column_view,
)


@pytest.fixture
def mock_column_profile_view() -> ColumnProfileView:
    mock_column_profile_view = Mock(wraps=ColumnProfileView)
    mock_column_profile_view.get_metric = MagicMock(return_value=None)
    return mock_column_profile_view  # type: ignore


def test_descriptive_statistics_returns_none_if_dist_metric_is_none(profile_view: DatasetProfileView) -> None:
    column_view = profile_view.get_column(col_name="any_feature")
    actual = _calculate_descriptive_statistics(column_view=column_view)
    assert actual is None


def test_get_count_metrics_should_return_none_if_column_view_is_none(
    mock_column_profile_view: ColumnProfileView,
) -> None:
    total_count, count_n, count_missing = _get_count_metrics_from_column_view(column_view=mock_column_profile_view)
    mock_column_profile_view.get_metric.assert_called_with("counts")  # type: ignore
    assert not count_n
    assert not count_missing


def test_count_metrics_should_return_count_values(profile_view: DatasetProfileView) -> None:
    column_view = profile_view.get_column(col_name="weight")
    assert column_view is not None

    total_count, count_n, count_missing = _get_count_metrics_from_column_view(column_view=column_view)

    assert isinstance(total_count, int)
    assert isinstance(count_n, int)
    assert isinstance(count_missing, int)


def test_dist_metrics_should_return_expected_values(profile_view: DatasetProfileView) -> None:
    column_view = profile_view.get_column(col_name="weight")
    assert column_view is not None

    stddev, mean, variance = _get_dist_metrics_from_column_view(column_view)

    assert isinstance(stddev, float)
    assert isinstance(variance, float)
    assert isinstance(mean, float)


def test_descriptive_statistics_returns_typed_dict(profile_view: DatasetProfileView) -> None:
    column_view = profile_view.get_column(col_name="weight")
    actual = _calculate_descriptive_statistics(column_view=column_view)

    assert actual is not None
    assert len(actual) == 5
    for key in actual.keys():
        assert key in ["stddev", "coefficient_of_variation", "sum", "variance", "mean"]


def test_descriptive_statistics_zero_mean(profile_view_zero_mean: DatasetProfileView) -> None:
    column_view = profile_view_zero_mean.get_column(col_name="weight")
    actual = _calculate_descriptive_statistics(column_view=column_view)

    assert actual is not None
    assert len(actual) == 5
    assert actual["coefficient_of_variation"] is None
    assert actual["sum"] == 0.0
    assert actual["mean"] == 0.0
