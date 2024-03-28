import pandas as pd
from pandas.api.types import is_integer_dtype
from pandas.api.types import is_string_dtype
from pandas.api.types import is_float_dtype

from rubrics.GradingRubric import GradingRubric


def buildExercise4Rubric() -> GradingRubric:
    def ensureColumns(df: pd.DataFrame) -> int:
        if len(df.columns) == 6:
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
            "id": is_integer_dtype,
            "producer": is_string_dtype,
            "model": is_string_dtype,
            "month": is_integer_dtype,
            "temperature": is_float_dtype,
            "battery_temperature": is_float_dtype,
        }

        for columnName in dtypes:
            if columnName in df.columns and dtypes[columnName](df[columnName]):
                result += 1

        return result

    def ensureTransformTemperature(df: pd.DataFrame) -> int:
        result = 0

        if not (
            "id" in df.columns
            or "month" in df.columns
            or "temperature" in df.columns
            or "battery_temperature" in df.columns
        ):
            return result

        g1 = df[(df["id"] == 85) & (df["month"] == 6)]
        g2 = df[(df["id"] == 7) & (df["month"] == 8)]

        if (
            g1.shape[0] == 1
            and abs(g1["temperature"].values[0] - 65.3) < 0.1
            and abs(g1["battery_temperature"].values[0] - 93.2) < 0.1
        ):
            result += 1

        if (
            g2.shape[0] == 1
            and abs(g2["temperature"].values[0] - 68.18) < 0.1
            and abs(g2["battery_temperature"].values[0] - 78.44) < 0.1
        ):
            result += 1

        return result

    def ensureNoEmptyValues(df: pd.DataFrame) -> int:
        if df.isna().sum().sum() == 0:
            return 2
        else:
            return 0

    rubric = GradingRubric("Exercise 4")

    rubric.addCheck(
        "Shape",
        ensureColumns,
        2,
        "Ensure all 6 columns of the source data are imported.",
    )
    rubric.addCheck(
        "Shape",
        ensureRows,
        2,
        "Ensure all 4872 complete data points of the source data are imported.",
    )
    rubric.addCheck(
        "Types", ensureTypes, 6, "Ensure all columns have a fitting basic data type."
    )
    rubric.addCheck(
        "Types",
        ensureTransformTemperature,
        2,
        "Ensure temperatures are correctly transformed to fahrenheit.",
    )
    rubric.addCheck(
        "Quality",
        ensureNoEmptyValues,
        2,
        "Ensure no empty values are included in the dataset.",
    )

    return rubric
