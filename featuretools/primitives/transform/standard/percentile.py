import numpy as np
import pandas as pd
from woodwork.column_schema import ColumnSchema
from woodwork.logical_types import (
    URL,
    Boolean,
    BooleanNullable,
    Categorical,
    Datetime,
    Double,
    EmailAddress,
    NaturalLanguage,
    Timedelta,
)

from featuretools.primitives.core.transform_primitive import TransformPrimitive
from featuretools.utils.common_tld_utils import COMMON_TLDS
from featuretools.utils.gen_utils import Library

class Percentile(TransformPrimitive):
    """Determines the percentile rank for each value in a list.

    Examples:
        >>> percentile = Percentile()
        >>> percentile([10, 15, 1, 20]).tolist()
        [0.5, 0.75, 0.25, 1.0]

        Nan values are ignored when determining rank

        >>> percentile([10, 15, 1, None, 20]).tolist()
        [0.5, 0.75, 0.25, nan, 1.0]
    """

    name = "percentile"
    uses_full_dataframe = True
    input_types = [ColumnSchema(semantic_tags={"numeric"})]
    return_type = ColumnSchema(semantic_tags={"numeric"})
    description_template = "the percentile rank of {}"

    def get_function(self):
        return lambda array: array.rank(pct=True)