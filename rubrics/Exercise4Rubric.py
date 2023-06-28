import pandas as pd
from pandas.api.types import is_integer_dtype
from pandas.api.types import is_string_dtype
from pandas.api.types import is_float_dtype

from rubrics.GradingRubric import GradingRubric

def buildExercise4Rubric() -> GradingRubric:
    def ensureColumns(df: pd.DataFrame) -> int:
        if len(df.columns) == 7:
            return 2
        else:
            return 0

    def ensureRows(df: pd.DataFrame) -> int:
        if len(df.index) == 4872:
            return 2
        else:
            return 0

    def ensureTypes(df: pd.DataFrame) -> int:
        result = 0

        dtypes = {
            'Geraet': is_integer_dtype,
			'Hersteller': is_string_dtype,
			'Model': is_string_dtype,
			'Monat': is_integer_dtype,
			'Temperatur': is_float_dtype,
			'Batterietemperatur': is_float_dtype,
			'Geraet aktiv': is_string_dtype,
        }

        for columnName in dtypes:
            if columnName in df.columns and dtypes[columnName](df[columnName]):
                result += 1

        return result

    def ensureTransformTemperature(df: pd.DataFrame) -> int:
        result = 0
        
        if not (
            'Geraet' in df.columns
            or 'Monat' in df.columns
            or 'Temperatur' in df.columns
            or 'Batterietemperatur' in df.columns
        ) :
            return
        
        g1 = df[(df['Geraet'] == 85) & (df['Monat'] == 6)]
        g2 = df[(df['Geraet'] == 7) & (df['Monat'] == 8)]

        if g1.shape[0] == 1 and abs(g1['Temperatur'].values[0] - 65.3) < 0.1 and abs(g1['Batterietemperatur'].values[0] - 93.2) < 0.1:
            result += 1

        if g2.shape[0] == 1 and abs(g2['Temperatur'].values[0] - 68.18) < 0.1 and abs(g2['Batterietemperatur'].values[0] - 78.44) < 0.1:
            result += 1

        return result

    def ensureNoEmptyValues(df: pd.DataFrame) -> int:
        if df.isna().sum().sum() == 0:
            return 2
        else:
            return 0


    rubric = GradingRubric('Exercise 4')

    rubric.addCheck("Shape", ensureColumns, 2, "Ensure all 7 columns of the source data are imported.")
    rubric.addCheck("Shape", ensureRows, 2, "Ensure all 4872 complete data points of the source data are imported.")
    rubric.addCheck("Types", ensureTypes, 7, "Ensure all columns have a fitting basic data type.")
    rubric.addCheck("Types", ensureTransformTemperature, 2, "Ensure temperatures are correctly transformed to celcius.")
    rubric.addCheck("Quality", ensureNoEmptyValues, 2, "Ensure no empty values are included in the dataset.")

    return rubric