import pandas as pd
from pandas.api.types import is_float_dtype
from pandas.api.types import is_string_dtype

from rubrics.GradingRubric import GradingRubric

def buildExercise3RubricGdp() -> GradingRubric:
    def ensureColumns(df: pd.DataFrame) -> int:
        if len(df.columns) == 2:
            return 2
        else:
            return 0

    def ensureRows(df: pd.DataFrame) -> int:
        if len(df.index) == 41:
            return 2
        else:
            return 0

    def ensureTypes(df: pd.DataFrame) -> int:
        result = 0

        dtypes = {
            "Country Code": is_string_dtype,
            "GDP per Capita": is_float_dtype,
        }

        for columnName in dtypes:
            if columnName in df.columns and dtypes[columnName](df[columnName]):
                result += 1

        return result

    def ensurePositiveInteger(df: pd.DataFrame) -> int:
        columns = [
            "GDP per Capita"
        ]

        df = df.reindex(columns=columns)

        # Convert all columns to numeric, coercing errors to NaN
        # Otherwise calling .min might error on strings
        df = df.apply(pd.to_numeric, errors="coerce")

        if float(df[columns].min().min()) > 0:
            return 2

        return 0

    def ensureNoEmptyValues(df: pd.DataFrame) -> int:
        if df.isna().sum().sum() == 0:
            return 2
        else:
            return 0

    rubric = GradingRubric()

    rubric.addCheck(
        "Shape",
        ensureColumns,
        2,
        "Ensure all 2 columns of the source data are imported.",
    )
    rubric.addCheck(
        "Shape",
        ensureRows,
        2,
        "Ensure all 41 complete data points of the source data are imported.",
    )
    rubric.addCheck(
        "Types", ensureTypes, 2, "Ensure all columns have a fitting basic data type."
    )
    rubric.addCheck(
        "Types",
        ensurePositiveInteger,
        2,
        "Ensure the gdp per capita column only has positive integers.",
    )
    rubric.addCheck(
        "Quality",
        ensureNoEmptyValues,
        2,
        "Ensure no empty values are included in the dataset.",
    )

    return rubric
