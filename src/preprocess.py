import pandas as pd
from textblob import TextBlob
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import zipfile
import csv

# VERSION 2.0
# nltk.download("punkt")
# nltk.download("stopwords")
# nltk.download("wordnet")

stop_words = set(stopwords.words("english"))


def load_raw_data(zip_file_path="src/assets/data/nuforc_reports.zip") -> pd.DataFrame:
    # unzip the file
    with zipfile.ZipFile(zip_file_path, "r") as z:
        z.extractall("src/assets/data")

    file_path = "src/assets/data/nuforc_reports.csv"
    return pd.read_csv(file_path)


def load_data() -> pd.DataFrame:

    # load the data
    df = pd.read_csv("src/assets/data/processed_data.csv")

    df["date_time"] = pd.to_datetime(df["date_time"], errors="coerce")

    # Convert "summary" to string
    df["summary"] = df["summary"].astype(str)

    # Convert duration to int
    df["duration"] = df["duration"].astype(int)

    return df


def remove_stop_words(text: str) -> str:
    words = word_tokenize(text)

    # remove punctuation

    filtered_words = [
        word for word in words if word.lower() not in stop_words and word.isalpha()
    ]

    return " ".join(filtered_words)


def sentiment_polarity(text: str) -> str:
    blob = TextBlob(text)
    return blob.sentiment.polarity


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
            # "text",
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

    # Sentiment analysis

    # Remove all stop words from the summary column
    df["summary"] = df["summary"].apply(remove_stop_words)

    # TODO : this shit is too long ... we will do it offline and save the CSV
    # Perform sentiment analysis on the summary column

    # VERSION 1.0
    df["sentiment"] = df["summary"].apply(sentiment_polarity)

    # VERSION 2.0
    # df['sentiment'] = df['summary'].apply(preprocess_and_analyze_sentiment)

    # Apply a threshold to the sentiment column, splitting it into three categories
    # [-1, -T] -> "negative"
    # (-T, +T) -> "neutral"
    # (+T, 1] -> "positive"

    def categorize_sentiment(s: float, treshold=0.10) -> str:
        if s <= -treshold:
            return "négatif"
        if s >= treshold:
            return "positif"

        return "neutre"

    df["sentiment"] = df["sentiment"].apply(lambda x: categorize_sentiment(x))

    # save to src/assets/data/processed_data.csv

    df.to_csv("src/assets/data/processed_data.csv", quoting=csv.QUOTE_STRINGS)

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


def filter_by_shapes(df: pd.DataFrame, shapes: list[str]) -> pd.DataFrame:

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

    # Keys : "Pre-1990" OR "1990" OR "2000" OR "2010" OR "Toutes"

    if decade == "Toutes":
        return df

    if decade == "Pre-1990":
        return df[df["date_time"].dt.year < 1990]

    min_year = int(decade)
    max_year = min_year + 9
    return df[
        (df["date_time"].dt.year >= min_year) & (df["date_time"].dt.year <= max_year)
    ]


def aggregate_by_hour(df: pd.DataFrame) -> pd.DataFrame:
    # Create a deep copy of the df called hourly_df
    hourly_df = df.copy()

    # Create a new column called "hour" that contains the hour of the date_time column
    hourly_df["hour"] = hourly_df["date_time"].dt.hour

    # drop all columns except "hour"
    hourly_df = hourly_df[["hour"]]
    hourly_df = hourly_df.groupby("hour").size().reset_index(name="counts")

    return hourly_df
