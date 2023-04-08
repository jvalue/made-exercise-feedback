import pandas as pd
from pandas.api.types import is_integer_dtype
from pandas.api.types import is_string_dtype
from pandas.api.types import is_float_dtype

from rubrics.GradingRubric import GradingRubric

def buildExercise1Rubric() -> GradingRubric:
    def ensureColumns(df: pd.DataFrame) -> int:
        if len(df.columns) == 13:
            return 2
        else:
            return 0

    def ensureRows(df: pd.DataFrame) -> int:
        if len(df.index) == 7847:
            return 2
        else:
            return 0

    def ensureTypes(df: pd.DataFrame) -> int:
        result = 0

        dtypes = {
            'column_1': is_integer_dtype,
            'column_2': is_string_dtype,
            'column_3': is_string_dtype,
            'column_4': is_string_dtype,
            'column_5': is_string_dtype,
            'column_6': is_string_dtype,
            'column_7': is_float_dtype,
            'column_8': is_float_dtype,
            'column_9': is_integer_dtype,
            'column_10': is_float_dtype,
            'column_11': is_string_dtype,
            'column_12': is_string_dtype,
            'geo_punkt': is_string_dtype,
            }

        for columnName in dtypes:
            if columnName in df.columns and dtypes[columnName](df[columnName]):
                result += 1

        return result


    rubric = GradingRubric('Exercise 1')

    rubric.addCheck("Shape", ensureColumns, 2, "Ensure all 13 columns of the source data are imported.")
    rubric.addCheck("Shape", ensureRows, 2, "Ensure all 7847 complete data points of the source data are imported.")
    rubric.addCheck("Types", ensureTypes, 13, "Ensure all columns have a fitting data type.")

    return rubric