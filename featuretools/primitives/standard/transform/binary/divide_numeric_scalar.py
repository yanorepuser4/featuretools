from woodwork.column_schema import ColumnSchema

from featuretools.primitives.base.transform_primitive_base import TransformPrimitive


class DivideNumericScalar(TransformPrimitive):
    """Divides each element in the list by a scalar.

    Description:
        Given a list of numeric values and a scalar, divide
        each value in the list by the scalar.

    Examples:
        >>> divide_numeric_scalar = DivideNumericScalar(value=2)
        >>> divide_numeric_scalar([3, 1, 2]).tolist()
        [1.5, 0.5, 1.0]
    """

    name = "divide_numeric_scalar"
    input_types = [ColumnSchema(semantic_tags={"numeric"})]
    return_type = ColumnSchema(semantic_tags={"numeric"})

    def __init__(self, value=1):
        self.value = value
        self.description_template = "the result of {{}} divided by {}".format(
            self.value,
        )

    def get_function(self):
        def divide_scalar(vals):
            return vals / self.value

        return divide_scalar

    def generate_name(self, base_feature_names):
        return "%s / %s" % (base_feature_names[0], str(self.value))
