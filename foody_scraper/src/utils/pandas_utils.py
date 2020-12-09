import pandas as pd
import numpy as np
from typing import Any, Generator, List, Optional
from pandas.api.types import is_datetime64_any_dtype, is_datetime64_ns_dtype, is_timedelta64_dtype, is_timedelta64_ns_dtype


def pandas_iter(
        df: pd.DataFrame,
        columns: List[str],
        mask: Optional[np.array] = None
) -> Generator[List[Any], None, None]:
    arrays = []

    for column in columns:
        srs = df.loc[:, column]

        if mask is not None:
            srs = srs[mask]

        if is_datetime64_any_dtype(srs) or is_datetime64_ns_dtype(srs):
            arrays.append(map(pd.Timestamp, srs.values))
        elif is_timedelta64_dtype(srs) or is_timedelta64_ns_dtype(srs):
            arrays.append(map(pd.Timedelta, srs.values))
        else:
            arrays.append(srs.values)
    yield from zip(*arrays)
