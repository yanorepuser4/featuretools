class All(AggregationPrimitive):
    """Calculates if all values are 'True' in a list.

    Description:
        Given a list of booleans, return `True` if all
        of the values are `True`.

    Examples:
        >>> all = All()
        >>> all([False, False, False, True])
        False
    """

    name = "all"
    input_types = [
        [ColumnSchema(logical_type=Boolean)],
        [ColumnSchema(logical_type=BooleanNullable)],
    ]
    return_type = ColumnSchema(logical_type=Boolean)
    stack_on_self = False
    compatibility = [Library.PANDAS, Library.DASK]
    description_template = "whether all of {} are true"

    def get_function(self, agg_type=Library.PANDAS):
        if agg_type == Library.DASK:

            def chunk(s):
                return s.agg(np.all)

            def agg(s):
                return s.agg(np.all)

            return dd.Aggregation(self.name, chunk=chunk, agg=agg)

        return np.all