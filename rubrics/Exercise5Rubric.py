import pandas as pd
from pandas.api.types import is_integer_dtype
from pandas.api.types import is_string_dtype
from pandas.api.types import is_bool_dtype
from pandas.api.types import is_float_dtype

from rubrics.GradingRubric import GradingRubric

def buildExercise5Rubric() -> GradingRubric:
    def ensureColumns(df: pd.DataFrame) -> int:
        if len(df.columns) == 5:
            return 2
        else:
            return 0

    def ensureRows(df: pd.DataFrame) -> int:
        if len(df.index) == 406:
            return 2
        else:
            return 0

    def ensureTypes(df: pd.DataFrame) -> int:
        result = 0

        dtypes = {
            'stop_id': is_integer_dtype,
			'stop_name': is_string_dtype,
			'stop_lat': is_float_dtype,
			'stop_lon': is_float_dtype,
			'zone_id': is_integer_dtype,
        }

        for columnName in dtypes:
            if columnName in df.columns and dtypes[columnName](df[columnName]):
                result += 1

        return result

    def ensureZoneId(df: pd.DataFrame) -> int:
        if 'zone_id' in df.columns and (df['zone_id'] == 2001).all():
            return 2
        else:
            return 0

    def ensureNoEmptyValues(df: pd.DataFrame) -> int:
        if df.isna().sum().sum() == 0:
            return 2
        else:
            return 0
        
    def ensureEncoding(df: pd.DataFrame) -> int:
        if 'Sickels Sägewerk' in df['stop_name'].values:
            return 1


    rubric = GradingRubric('Exercise 5')

    rubric.addCheck("Shape", ensureColumns, 2, "Ensure all 5 columns of the source data are imported.")
    rubric.addCheck("Shape", ensureRows, 2, "Ensure all 406 complete data points of the source data are imported.")
    rubric.addCheck("Types", ensureTypes, 5, "Ensure all columns have a fitting basic data type.")
    rubric.addCheck("Quality", ensureNoEmptyValues, 2, "Ensure no empty values are included in the dataset.")
    rubric.addCheck("Quality", ensureZoneId, 2, "Ensure only stops from the right zone are included in the dataset.")
    rubric.addCheck("Quality", ensureEncoding, 1, "Ensure text data is encoded correctly to maintain german umlauts.")

    return rubric