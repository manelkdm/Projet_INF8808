import pandas as pd


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
    df = df.drop("country", axis=1)

    # Cast the date_time column to a format dd-mm-yyyy hh:mm
    df["date_time"] = pd.to_datetime(df["date_time"], errors="coerce")

    # convert the duration into seconds
    df["duration"] = df["duration"].apply(lambda x: convert_to_seconds(x))
    df = df.dropna(subset=["duration"])

    # convert the shape to lowercase
    primary_shapes = ["light", "circle", "triangle", "fireball"]
    df["shape"] = df["shape"].apply(lambda x: x.lower())
    df["shape"] = df["shape"].apply(lambda x: x if x in primary_shapes else "other")

    return df


def convert_to_seconds(duration) -> float:

    # First we split the duration by space
    duration = duration.lower()
    # duration = duration.split()

    # remove all non alphanumeric characters
    duration = "".join([c for c in duration if c.isalnum() or c.isspace() or c == "-"])

    # Then we lowercase the duration

    time_keywords = {
        "s": "s",
        "se": "s",
        "sec": "s",
        "second": "s",
        "seconds": "s",
        "m": "m",
        "mi": "m",
        "mii": "m",
        "min": "m",
        "mins": "m",
        "mon": "m",
        "mnutes": "m",
        "kinutes": "m",
        "ninutes": "m",
        "minute": "m",
        "minutes": "m",
        "h": "h",
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

    time_values = {
        "s": 1,
        "m": 60,
        "h": 60 * 60,
        "d": 24 * 60 * 60,
        "w": 7 * 24 * 60 * 60,
        "mo": 30 * 24 * 60 * 60,
        "y": 365 * 24 * 60 * 60,
    }

    # find if there is any number in the duration
    has_number = False

    for word in duration:
        if word.isnumeric():
            has_number = True
            break

    has_keyword = False

    for word in duration.split():
        if word in time_keywords:
            has_keyword = True
            break

    if has_keyword and has_number:
        duration_1 = [time_keywords.get(word, word) for word in duration.split()]

        # Find all occurences of X-Y where X and Y are numbers
        for i, dur in enumerate(duration_1):

            if "-" in dur:

                candidate = dur.split("-")
                if (
                    len(candidate) == 2
                    and candidate[0].isnumeric()
                    and candidate[1].isnumeric()
                ):
                    num_1 = int(candidate[0])
                    num_2 = int(candidate[1])
                    mean = int((num_1 + num_2) / 2)
                    duration_1[i] = str(mean)

        duration_2 = [
            word for word in duration_1 if word.isnumeric() or word in time_values
        ]

        # print(f"{d_1:<20} -> {d_2:<20}")

        total_seconds = 0

        for i in range(len(duration_2) - 1):
            val_1 = duration_2[i]
            val_2 = duration_2[i + 1]

            if val_1.isnumeric() and val_2 in time_values:

                if val_1 == "2½":
                    val_1 = 2
                total_seconds += int(val_1) * time_values[val_2]

        return total_seconds if total_seconds > 0 else None

    else:
        return None


def filter_by_shape(df: pd.DataFrame, shapes: list[str]) -> pd.DataFrame:

    # Keys: subset of "light", "circle", "triangle", "fireball", "other"

    if not shapes:
        return df

    return df[df["shape"].isin(shapes)]


def filter_by_duration(df: pd.DataFrame, duration: str = "all"):

    # Keys : "short" OR "long" OR "all"

    if duration == "all":
        return df

    if duration == "short":
        return df[df["duration"] < 60]

    if duration == "long":
        return df[df["duration"] >= 60]

    return df


def filter_by_decade(df: pd.DataFrame, decade: str = "Toutes") -> pd.DataFrame:

    # Keys : "1990" OR "2000" OR "2010" OR "Toutes"
    if decade == "Toutes":
        return df

    min_year = int(decade)
    max_year = min_year + 9
    return df[
        (df["date_time"].dt.year >= min_year) & (df["date_time"].dt.year <= max_year)
    ]


def restructure_df(df: pd.DataFrame) -> pd.DataFrame:

    # Create a deep copy of the df called yearly_df
    yearly_df = df.copy()

    # Create a new column called "year" that contains the year of the date_time column
    yearly_df["year"] = yearly_df["date_time"].dt.year
    yearly_df["month"] = yearly_df["date_time"].dt.month

    # drop all columns except "year" and "month"
    yearly_df = yearly_df[["year", "month"]]
    yearly_df = yearly_df.groupby(["year", "month"]).size().reset_index(name="counts")

    # Create a new df with rows = year, columns = month, values = count of observations
    yearly_df = yearly_df.pivot(index="year", columns="month", values="counts")
    yearly_df = yearly_df.fillna(0).astype(int)

    return yearly_df


def aggregate_by_hour(df: pd.DataFrame) -> pd.DataFrame:
    # Create a deep copy of the df called hourly_df
    hourly_df = df.copy()

    # Create a new column called "hour" that contains the hour of the date_time column
    hourly_df["hour"] = hourly_df["date_time"].dt.hour

    # drop all columns except "hour"
    hourly_df = hourly_df[["hour"]]
    hourly_df = hourly_df.groupby("hour").size().reset_index(name="counts")

    return hourly_df


if __name__ == "__main__":
    df = load_data()
    df = preprocess(df)

    print(df.shape)
    print(df.dtypes)

    print("-" * 120)
    hdf = aggregate_by_hour(df)

    print(hdf)

    # print unique values of the column "shape"
    # print(df["shape"].unique())

    # Print the first 5 values of the column date_time
    # print(df["date_time"].head(50))

    # Print the unique cities of the country called "U"
    # print(df[df["country"] == "U"]["summary"])
