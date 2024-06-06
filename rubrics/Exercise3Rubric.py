import pandas as pd
from pandas.api.types import is_integer_dtype
from pandas.api.types import is_string_dtype

from rubrics.GradingRubric import GradingRubric


def buildExercise3Rubric() -> GradingRubric:
    def ensureColumns(df: pd.DataFrame) -> int:
        if len(df.columns) == 7:
            return 2
        else:
            return 0

    def ensureRows(df: pd.DataFrame) -> int:
        if len(df.index) == 1448:
            return 2
        else:
            return 0

    def ensureTypes(df: pd.DataFrame) -> int:
        result = 0

        dtypes = {
            "year": is_integer_dtype,
            "month": is_string_dtype,
            "goods_id": is_string_dtype,
            "goods_name": is_string_dtype,
            "goods_source": is_string_dtype,
            "abroad": is_integer_dtype,
            "total": is_integer_dtype,
        }

        for columnName in dtypes:
            if columnName in df.columns and dtypes[columnName](df[columnName]):
                result += 1

        return result

    def ensureEncoding(df: pd.DataFrame) -> int:
        if "goods_source" in df.columns and "Lüneburg" in df["goods_source"].values:
            return 2
        return 0

    def ensureValidGoodsId(df: pd.DataFrame) -> int:
        if (
            "goods_id" in df.columns
            and df["goods_id"].str.match(r"NST7-[0-9A-Z]{3}").all()
        ):
            return 2
        else:
            return 0

    def ensureValidPositiveInteger(df: pd.DataFrame) -> int:
        columns = [
            "year",
            "abroad",
            "total",
        ]

        df = df.reindex(columns=columns)

        # Convert all columns to numeric, coercing errors to NaN
        # Otherwise calling .min might error on strings
        df = df.apply(pd.to_numeric, errors="coerce")

        if int(df[columns].min().min()) > 0:
            return 2

        return 0

    def ensureNoEmptyValues(df: pd.DataFrame) -> int:
        if df.isna().sum().sum() == 0:
            return 2
        else:
            return 0

    rubric = GradingRubric("Exercise 3")

    rubric.addCheck(
        "Shape",
        ensureColumns,
        2,
        "Ensure all 7 columns of the source data are imported.",
    )
    rubric.addCheck(
        "Shape",
        ensureRows,
        2,
        "Ensure all 1448 complete data points of the source data are imported.",
    )
    rubric.addCheck(
        "Types", ensureTypes, 7, "Ensure all columns have a fitting basic data type."
    )
    rubric.addCheck(
        "Types",
        ensureValidGoodsId,
        2,
        "Ensure the goods_id column is exactly formatted correctly.",
    )
    rubric.addCheck(
        "Types",
        ensureValidPositiveInteger,
        2,
        "Ensure the numeric columns only have positive integers.",
    )
    rubric.addCheck(
        "Quality",
        ensureEncoding,
        2,
        "Ensure text data is encoded correctly to maintain german umlauts.",
    )
    rubric.addCheck(
        "Quality",
        ensureNoEmptyValues,
        2,
        "Ensure no empty values are included in the dataset.",
    )

    return rubric
