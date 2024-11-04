import pandas as pd
from pandas.api.types import is_integer_dtype
from pandas.api.types import is_string_dtype
from pandas.api.types import is_float_dtype

from rubrics.GradingRubric import GradingRubric


def buildExercise1Rubric() -> GradingRubric:
    def ensureColumns(df: pd.DataFrame) -> int:
        if len(df.columns) == 9:
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
            "Lfd. Nummer": is_integer_dtype,
            "Name des Flughafens": is_string_dtype,
            "Ort": is_string_dtype,
            "Land": is_string_dtype,
            "IATA": is_string_dtype,
            "ICAO": is_string_dtype,
            "Latitude": is_float_dtype,
            "Longitude": is_float_dtype,
            "Altitude": is_integer_dtype,
            # "Zeitzone": is_float_dtype,
            # "DST": is_string_dtype,
            # "Zeitzonen-Datenbank": is_string_dtype,
            # "geo_punkt": is_string_dtype,
        }

        for columnName in dtypes:
            if columnName in df.columns and dtypes[columnName](df[columnName]):
                result += 1

        return result

    rubric = GradingRubric()

    rubric.addCheck(
        "Shape",
        ensureColumns,
        2,
        "Ensure all 9 columns of the source data are imported.",
    )
    rubric.addCheck(
        "Shape",
        ensureRows,
        2,
        "Ensure all 7847 complete data points of the source data are imported.",
    )
    rubric.addCheck(
        "Types", ensureTypes, 9, "Ensure all columns have a fitting data type."
    )

    return rubric
