from datetime import datetime, timedelta

import numpy as np
import pandas as pd
from dask import dataframe as dd
from scipy import stats
from woodwork.column_schema import ColumnSchema
from woodwork.logical_types import (
    Boolean,
    BooleanNullable,
    Datetime,
    Double,
    IntegerNullable,
)
from featuretools.primitives.core.aggregation_primitive import AggregationPrimitive

from featuretools.utils import convert_time_units
from featuretools.utils.gen_utils import Library

class NumTrue(AggregationPrimitive):
    """Counts the number of `True` values.

    Description:
        Given a list of booleans, return the number
        of `True` values. Ignores 'NaN'.

    Examples:
        >>> num_true = NumTrue()
        >>> num_true([True, False, True, True, None])
        3
    """

    name = "num_true"
    input_types = [
        [ColumnSchema(logical_type=Boolean)],
        [ColumnSchema(logical_type=BooleanNullable)],
    ]
    return_type = ColumnSchema(logical_type=IntegerNullable, semantic_tags={"numeric"})
    default_value = 0
    stack_on = []
    stack_on_exclude = []
    compatibility = [Library.PANDAS, Library.DASK]
    description_template = "the number of times {} is true"

    def get_function(self, agg_type=Library.PANDAS):
        if agg_type == Library.DASK:

            def chunk(s):
                chunk_sum = s.agg(np.sum)
                if chunk_sum.dtype == "bool":
                    chunk_sum = chunk_sum.astype("int64")
                return chunk_sum

            def agg(s):
                return s.agg(np.sum)

            return dd.Aggregation(self.name, chunk=chunk, agg=agg)

        return np.sum