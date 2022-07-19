import holidays
import numpy as np
import pandas as pd
from woodwork.column_schema import ColumnSchema
from woodwork.logical_types import (
    AgeFractional,
    BooleanNullable,
    Categorical,
    Datetime,
    Ordinal,
)

from featuretools.primitives.core.transform_primitive import TransformPrimitive
from featuretools.primitives.utils import HolidayUtil
from featuretools.utils import convert_time_units
from featuretools.utils.gen_utils import Library

class DayOfYear(TransformPrimitive):
    """Determines the ordinal day of the year from the given datetime

    Description:
        For a list of dates, return the ordinal day of the year
        from the given datetime.

    Examples:
        >>> from datetime import datetime
        >>> dates = [datetime(2019, 1, 1),
        ...          datetime(2020, 12, 31),
        ...          datetime(2020, 2, 28)]
        >>> dayOfYear = DayOfYear()
        >>> dayOfYear(dates).tolist()
        [1, 366, 59]
    """

    name = "day_of_year"
    input_types = [ColumnSchema(logical_type=Datetime)]
    return_type = ColumnSchema(
        logical_type=Ordinal(order=list(range(1, 367))),
        semantic_tags={"category"},
    )
    compatibility = [Library.PANDAS, Library.DASK, Library.SPARK]
    description_template = "the day of year from {}"

    def get_function(self):
        def dayOfYear(vals):
            return vals.dt.dayofyear

        return dayOfYear