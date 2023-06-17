import pandas as pd
from pandas.api.types import is_integer_dtype
from pandas.api.types import is_string_dtype

from rubrics.GradingRubric import GradingRubric

def buildExercise3Rubric() -> GradingRubric:
    def ensureColumns(df: pd.DataFrame) -> int:
        if len(df.columns) == 10:
            return 2
        else:
            return 0

    def ensureRows(df: pd.DataFrame) -> int:
        if len(df.index) == 399:
            return 2
        else:
            return 0

    def ensureTypes(df: pd.DataFrame) -> int:
        result = 0

        dtypes = {
            'date': is_string_dtype,
            'CIN': is_string_dtype,
            'name': is_string_dtype,
            'petrol': is_integer_dtype,
            'diesel': is_integer_dtype,
            'gas': is_integer_dtype,
            'electro': is_integer_dtype,
            'hybrid': is_integer_dtype,
            'plugInHybrid': is_integer_dtype,
            'others': is_integer_dtype
        }

        for columnName in dtypes:
            if columnName in df.columns and dtypes[columnName](df[columnName]):
                result += 1

        return result

    def ensureEncoding(df: pd.DataFrame) -> int:
        if 'Düren, Landkreis' in df['name'].values:
            return 2
        return 0

    def ensureValidCommunityIdentificationNumber(df: pd.DataFrame) -> int:
        if 'CIN' in df.columns and df['CIN'].str.match(r'.{5}').all():
            return 2
        else:
            return 0
        
    def ensureValidPositiveInteger(df: pd.DataFrame) -> int:
        columns = [
            'petrol',
            'diesel',
            'gas',
            'electro',
            'hybrid',
            'plugInHybrid',
            'others'
        ]

        if int(df[columns].min().min()) > 0:
            return 2
        
        return 0

    def ensureNoEmptyValues(df: pd.DataFrame) -> int:
        if df.isna().sum().sum() == 0:
            return 2
        else:
            return 0


    rubric = GradingRubric('Exercise 3')

    rubric.addCheck("Shape", ensureColumns, 2, "Ensure all 10 columns of the source data are imported.")
    rubric.addCheck("Shape", ensureRows, 2, "Ensure all 399 complete data points of the source data are imported.")
    rubric.addCheck("Types", ensureTypes, 10, "Ensure all columns have a fitting basic data type.")
    rubric.addCheck("Types", ensureValidCommunityIdentificationNumber, 2, "Ensure the CIN column is exactly five characters long.")
    rubric.addCheck("Types", ensureValidPositiveInteger, 2, "Ensure the numeric columns only have positive integers.")
    rubric.addCheck("Quality", ensureEncoding, 2, "Ensure text data is encoded correctly to maintain german umlauts.")
    rubric.addCheck("Quality", ensureNoEmptyValues, 2, "Ensure no empty values are included in the dataset.")

    return rubric