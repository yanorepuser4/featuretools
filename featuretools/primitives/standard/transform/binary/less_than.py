import numpy as np
import pandas as pd
from woodwork.column_schema import ColumnSchema
from woodwork.logical_types import BooleanNullable, Datetime, Ordinal

from featuretools.primitives.base.transform_primitive_base import TransformPrimitive


class LessThan(TransformPrimitive):
    """Determines if values in one list are less than another list.

    Description:
        Given a list of values X and a list of values Y, determine
        whether each value in X is less than each corresponding value
        in Y. Equal pairs will return `False`.

    Examples:
        >>> less_than = LessThan()
        >>> less_than([2, 1, 2], [1, 2, 2]).tolist()
        [False, True, False]
    """

    name = "less_than"
    input_types = [
        [
            ColumnSchema(semantic_tags={"numeric"}),
            ColumnSchema(semantic_tags={"numeric"}),
        ],
        [ColumnSchema(logical_type=Datetime), ColumnSchema(logical_type=Datetime)],
        [ColumnSchema(logical_type=Ordinal), ColumnSchema(logical_type=Ordinal)],
    ]
    return_type = ColumnSchema(logical_type=BooleanNullable)

    description_template = "whether {} is less than {}"

    def get_function(self):
        def less_than(val1, val2):
            val1_is_categorical = isinstance(val1.dtype, pd.CategoricalDtype)
            val2_is_categorical = isinstance(val2.dtype, pd.CategoricalDtype)
            if val1_is_categorical and val2_is_categorical:
                if not all(val1.cat.categories == val2.cat.categories):
                    return val1.where(pd.isnull, np.nan)
            elif val1_is_categorical or val2_is_categorical:
                # This can happen because CFM does not set proper dtypes for intermediate
                # features, so some agg features that should be Ordinal don't yet have correct type.
                return val1.where(pd.isnull, np.nan)
            return val1 < val2

        return less_than

    def generate_name(self, base_feature_names):
        return "%s < %s" % (base_feature_names[0], base_feature_names[1])
