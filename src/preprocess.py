import pandas as pd
import numpy as np


def load_data(file_path="src/assets/data/nuforc_reports.csv") -> pd.DataFrame:
    return pd.read_csv(file_path)


def preprocess(df: pd.DataFrame) -> pd.DataFrame:

    # drop the rows with missing values
    df = df.dropna()

    #  keep the columns that are needed
    df = df[
        [
            "summary",
            "country",
            "city",
            "state",
            "date_time",
            "shape",
            "duration",
            "text",
            "city_latitude",
            "city_longitude",
        ]
    ]

    # Keep only the rows where the country is in a list
    countries = ["USA", "usa", "USAv", "Usa", "USAUSA", "U", "Untied States of America"]

    df = df[df["country"].isin(countries)]

    # drop the country column
    df = df.drop("country", axis=1)

    # Cast the date_time column to a format dd-mm-yyyy hh:mm
    df["date_time"] = pd.to_datetime(df["date_time"], errors="coerce")

    # convert the duration into seconds
    df = convert_durations(df)
    df["duration"] = df["duration"].apply(lambda x: convert_to_seconds(x))

    # convert the shape to lowercase
    df["shape"] = df["shape"].apply(lambda x: x.lower())

    return df


def convert_durations(df: pd.DataFrame) -> pd.DataFrame:

    # First we split the duration by space
    duration = duration.lower()
    # duration = duration.split()

    # Then we lowercase the duration
    time_keywords = ["second", "minute", "hour", "day", "week", "month", "year"]

    time_keywords = {
        "se": "s",
        "sec": "s",
        "second": "s",
        "seconds": "s",
        "mi": "m",
        "mii": "m",
        "min": "m",
        "mon": "m",
        "mnutes": "m",
        "k": "m",
        "ninutes": "m",
        "minute": "m",
        "minutes": "m",
        "hr": "h",
        "hrs": "h",
        "hour": "h",
        "hours": "h",
        "day": "d",
        "days": "d",
        "week": "w",
        "month": "mo",
        "months": "mo",
        "yrs": "y",
        "year": "y",
    }

    # find if there is any number in the duration
    has_number = False

    for word in duration:
        if word.isnumeric():
            has_number = True
            break

    has_keyword = False

    for keyword in time_keywords:
        if keyword in duration:
            has_keyword = True
            break

    if not has_keyword and has_number:
        print(duration)


if __name__ == "__main__":
    df = load_data()
    df = preprocess(df)
    # print(df.head())
    print(df.shape)
    print(df.dtypes)

    # print unique values of the column "shape"
    # print(df["shape"].unique())

    # Print the first 5 values of the column date_time
    print(df["duration"].head(100))

    # Print the unique cities of the country called "U"
    # print(df[df["country"] == "U"]["summary"])
