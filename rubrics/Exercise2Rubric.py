import pandas as pd
from pandas.api.types import is_integer_dtype
from pandas.api.types import is_string_dtype
from pandas.api.types import is_float_dtype

from rubrics.GradingRubric import GradingRubric

def buildExercise2Rubric() -> GradingRubric:
    def ensureColumns(df: pd.DataFrame) -> int:
        if len(df.columns) == 9:
            return 2
        else:
            return 0

    def ensureRows(df: pd.DataFrame) -> int:
        if len(df.index) == 5392:
            return 2
        else:
            return 0

    def ensureColumnsDropped(df: pd.DataFrame) -> int:
        if 'Status' in df.columns:
            return 0
        else:
            return 1

    def ensureTypes(df: pd.DataFrame) -> int:
        result = 0

        dtypes = {
            'EVA_NR': is_integer_dtype,
            'DS100': is_string_dtype,
            'IFOPT': is_string_dtype,
            'NAME': is_string_dtype,
            'Verkehr': is_string_dtype,
            'Laenge': is_float_dtype,
            'Breite': is_float_dtype,
            'Betreiber_Name': is_string_dtype,
            'Betreiber_Nr': is_integer_dtype
            }

        for columnName in dtypes:
            if columnName in df.columns and dtypes[columnName](df[columnName]):
                result += 1

        return result

    def ensureValidVerkehr(df: pd.DataFrame) -> int:
        if 'Verkehr' in df.columns and df['Verkehr'].str.match(r'FV|RV|nur DPN').all():
            return 2
        else:
            return 0
    
    def ensureValidIFOPT(df: pd.DataFrame) -> int:
        if 'IFOPT' in df.columns and df['IFOPT'].str.match(r'^[a-z]{2}:\d+:\d+(:\d+)?$').all():
            return 2
        else:
            return 0

    def ensureValidLaenge(df: pd.DataFrame) -> int:
        if 'Laenge' in df.columns and df['Laenge'].between(-90, 90, inclusive='both').all():
            return 2
        else:
            return 0
    
    def ensureValidBreite(df: pd.DataFrame) -> int:
        if 'Breite' in df.columns and df['Breite'].between(-90, 90, inclusive='both').all():
            return 2
        else:
            return 0

    def ensureNoEmptyValues(df: pd.DataFrame) -> int:
        if df.isna().sum().sum() == 0:
            return 2
        else:
            return 0


    rubric = GradingRubric('Exercise 2')

    rubric.addCheck("Shape", ensureColumns, 2, "Ensure all 9 columns of the source data are imported.")
    rubric.addCheck("Shape", ensureRows, 2, "Ensure all 5392 complete data points of the source data are imported.")
    rubric.addCheck("Shape", ensureColumnsDropped, 1, "Ensure the Status column is dropped.")
    rubric.addCheck("Types", ensureTypes, 9, "Ensure all columns have a fitting basic data type.")
    rubric.addCheck("Types", ensureValidVerkehr, 2, "Ensure the Verkehr column only contains 'FV', 'RV' or 'nur DPN'.")
    rubric.addCheck("Types", ensureValidIFOPT, 2, "Ensure the IFOPT column only contains values according to the following format: <exactly two characters>:<any amount of numbers>:<any amount of numbers><optionally another colon followed by any amount of numbers>.")
    rubric.addCheck("Types", ensureValidLaenge, 2, "Ensure the Laenge column only contains values that are valid geographical coordinates.")
    rubric.addCheck("Types", ensureValidBreite, 2, "Ensure the Breite column only contains values that are valid geographical coordinates.")
    rubric.addCheck("Quality", ensureNoEmptyValues, 2, "Ensure no empty values are included in the dataset.")

    return rubric