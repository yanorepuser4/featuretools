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

class NumWords(TransformPrimitive):
    """Determines the number of words in a string by counting the spaces.

    Examples:
        >>> num_words = NumWords()
        >>> num_words(['This is a string',
        ...            'Two words',
        ...            'no-spaces',
        ...            'Also works with sentences. Second sentence!']).tolist()
        [4, 2, 1, 6]
    """

    name = "num_words"
    input_types = [ColumnSchema(logical_type=NaturalLanguage)]
    return_type = ColumnSchema(semantic_tags={"numeric"})
    compatibility = [Library.PANDAS, Library.DASK, Library.SPARK]
    description_template = "the number of words in {}"

    def get_function(self):
        def word_counter(array):
            return array.fillna("").str.count(" ") + 1

        return word_counter