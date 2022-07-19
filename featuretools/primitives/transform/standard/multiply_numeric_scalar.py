import numpy as np
import pandas as pd
import pandas.api.types as pdtypes
from woodwork.column_schema import ColumnSchema
from woodwork.logical_types import Boolean, BooleanNullable, Datetime, Ordinal

from featuretools.primitives.core.transform_primitive import TransformPrimitive
from featuretools.utils.gen_utils import Library

class MultiplyNumericScalar(TransformPrimitive):
    """Multiply each element in the list by a scalar.

    Description:
        Given a list of numeric values and a scalar, multiply
        each value in the list by the scalar.

    Examples:
        >>> multiply_numeric_scalar = MultiplyNumericScalar(value=2)
        >>> multiply_numeric_scalar([3, 1, 2]).tolist()
        [6, 2, 4]
    """

    name = "multiply_numeric_scalar"
    input_types = [ColumnSchema(semantic_tags={"numeric"})]
    return_type = ColumnSchema(semantic_tags={"numeric"})
    compatibility = [Library.PANDAS, Library.DASK, Library.SPARK]

    def __init__(self, value=1):
        self.value = value
        self.description_template = "the product of {{}} and {}".format(self.value)

    def get_function(self):
        def multiply_scalar(vals):
            return vals * self.value

        return multiply_scalar

    def generate_name(self, base_feature_names):
        return "%s * %s" % (base_feature_names[0], str(self.value))