import logging
import os.path
import time
from typing import Any, Dict, Mapping, Optional

from .column_profile import ColumnProfile
from .schema import DatasetSchema
from .stubs import pd
from .view import DatasetProfileView

logger = logging.getLogger(__name__)

_LARGE_CACHE_SIZE_LIMIT = 1024 * 100


class DatasetProfile(object):
    """Dataset profile represents a collection of in-memory profiling stats for a dataset."""

    def __init__(self, schema: Optional[DatasetSchema] = None):
        """
        Init func.

        Args:
            schema: a :class:`DatasetSchema` object that
        """

        if schema is None:
            schema = DatasetSchema()
        self._schema = schema
        self._columns: Dict[str, ColumnProfile] = dict()

    def track(
        self,
        obj: Any = None,
        *,
        pandas: Optional[pd.DataFrame] = None,
        row: Optional[Mapping[str, Any]] = None,
    ) -> None:
        if obj is not None:
            if pandas is not None:
                raise ValueError("Cannot pass both obj and pandas params")
            if row is not None:
                raise ValueError("Cannot pass both obj and row params")

            if isinstance(obj, pd.DataFrame):
                pandas = obj
            elif isinstance(obj, (dict, Dict, Mapping)):
                row = obj

        if pandas is not None and row is not None:
            raise ValueError("Cannot pass both pandas and row params")

        # TODO: do this less frequently when operating at row level
        dirty = self._schema.resolve(pandas=pandas, row=row)
        if dirty:
            new_cols = self._schema.get_col_names().difference(self._columns.keys())
            for col in new_cols:
                col_schema = self._schema.get(col)
                if col_schema:
                    self._columns[col] = ColumnProfile(name=col, schema=col_schema, cache_size=self._schema.cache_size)
                else:
                    logger.warning("Encountered a column without schema: %s", col)

        if pandas is not None:
            for k in pandas.keys():
                self._columns[k].track_column(pandas[k])
            return

        if row is not None:
            for k in row.keys():
                self._columns[k].track_column(row[k])
            return

        raise NotImplementedError

    def view(self) -> DatasetProfileView:
        columns = {}
        for c_name, c in self._columns.items():
            columns[c_name] = c.view()
        return DatasetProfileView(columns=columns)

    def flush(self) -> None:
        for col in self._columns.values():
            col.flush()

    def write(self, path_or_base_dir: str) -> None:
        if not path_or_base_dir.endswith(".bin"):
            output_path = os.path.join(path_or_base_dir, f"profile.{int(round(time.time() * 1000))}.bin")
        else:
            output_path = path_or_base_dir

        self.view().write(output_path)
        logger.debug("Wrote profile to path: %s", output_path)

    @classmethod
    def read(cls, input_path: str) -> DatasetProfileView:
        return DatasetProfileView.read(input_path)

    def __repr__(self) -> str:
        return f"DatasetProfile({len(self._columns)} columns). Schema: {str(self._schema)}"