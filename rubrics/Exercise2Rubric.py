import pandas as pd
from pandas.api.types import is_integer_dtype
from pandas.api.types import is_string_dtype

from rubrics.GradingRubric import GradingRubric


def buildExercise2Rubric() -> GradingRubric:
    def ensureColumns(df: pd.DataFrame) -> int:
        if len(df.columns) == 6:
            return 2
        else:
            return 0

    def ensureRows(df: pd.DataFrame) -> int:
        if len(df.index) == 175:
            return 2
        else:
            return 0

    def ensureColumnsDropped(df: pd.DataFrame) -> int:
        if "baumart_deutsch" in df.columns:
            return 0
        else:
            return 1

    def ensureTypes(df: pd.DataFrame) -> int:
        result = 0

        dtypes = {
            "lfd_nr": is_integer_dtype,
            "stadtteil": is_string_dtype,
            "standort": is_string_dtype,
            "baumart_botanisch": is_string_dtype,
            "id": is_string_dtype,
            "baumfamilie": is_string_dtype,
        }

        for columnName in dtypes:
            if columnName in df.columns and dtypes[columnName](df[columnName]):
                result += 1

        return result

    def ensureValidStadtteil(df: pd.DataFrame) -> int:
        if "stadtteil" in df.columns and df["stadtteil"].str.match(r"Furth-[.]*").all():
            return 2
        else:
            return 0

    def ensureValidId(df: pd.DataFrame) -> int:
        if (
            "id" in df.columns
            and df["id"].str.match(r"^[0-9]{1,3}\.[0-9]+, [0-9]{1,3}\.[0-9]+$").all()
        ):
            return 2
        else:
            return 0

    def ensureNoEmptyValues(df: pd.DataFrame) -> int:
        if df.isna().sum().sum() == 0:
            return 2
        else:
            return 0

    rubric = GradingRubric("Exercise 2")

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
        "Ensure all 175 complete data points of the source data are imported.",
    )
    rubric.addCheck(
        "Shape",
        ensureColumnsDropped,
        1,
        "Ensure the baumart_deutsch column is dropped.",
    )
    rubric.addCheck(
        "Types", ensureTypes, 6, "Ensure all columns have a fitting basic data type."
    )
    rubric.addCheck(
        "Types",
        ensureValidStadtteil,
        2,
        "Ensure the stadtteil column only contains valid values.",
    )
    rubric.addCheck(
        "Types",
        ensureValidId,
        2,
        "Ensure the id column only contains valid values.",
    )
    rubric.addCheck(
        "Quality",
        ensureNoEmptyValues,
        2,
        "Ensure no empty values are included in the dataset.",
    )

    return rubric
