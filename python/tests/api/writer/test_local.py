from unittest.mock import Mock

import pytest

from whylogs.api.writer.local import LocalWriter


class TestLocalWriter(object):
    @pytest.fixture
    def local_writer(self):
        writer = LocalWriter(base_dir="test_dir", base_name="test_name")
        return writer

    @pytest.fixture
    def mocked_profile_view(self):
        profile_view = Mock()
        profile_view.write = Mock()
        profile_view.creation_timestamp = Mock()
        return profile_view

    def test_should_write_to_default_dir_if_dest_is_none(self, local_writer, mocked_profile_view):
        local_writer.write(profile=mocked_profile_view, dest=None)
        mocked_profile_view.write.assert_called_once_with(
            f"test_dir/test_name_{mocked_profile_view.creation_timestamp}.bin"
        )

    def test_should_write_to_defined_destination(self, local_writer, mocked_profile_view):
        local_writer.write(profile=mocked_profile_view, dest="some_dest.bin")
        mocked_profile_view.write.assert_called_once_with("test_dir/some_dest.bin")
