import pandas as pd
from textblob import TextBlob
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import zipfile
import csv
import os
from preprocess_constants import TIME_KEYWORDS, TIME_VALUES


def load_raw_data(zip_file_path="assets/data/nuforc_reports.zip") -> pd.DataFrame:
    # unzip the file
    with zipfile.ZipFile(zip_file_path, "r") as z:
        z.extractall("assets/data")

    file_path = "assets/data/nuforc_reports.csv"
    return pd.read_csv(file_path)


def load_data() -> pd.DataFrame:

    df = pd.read_csv("assets/data/processed_data.csv")

    # Convert columns to the right type
    df["date_time"] = pd.to_datetime(df["date_time"], errors="coerce")
    df["summary"] = df["summary"].astype(str)
    df["duration"] = df["duration"].astype(int)

    return df

def load_events() -> pd.DataFrame:

    events_db = pd.read_csv("assets/data/events.csv")
    return events_db


def preprocess_raw_text(text: str, stop_words, lemmatizer) -> str:
    """
    This function preprocesses the text by removing stopwords, punctuation, and lemmatizing the words.

    For example, the text "I am running." will be transformed into "run".
    """

    # Preprocess the text
    words = word_tokenize(text)
    words = [w.lower() for w in words]
    filtered_words = [w for w in words if w.lower() not in stop_words and w.isalpha()]

    # Lemmatize the words
    filtered_words = [lemmatizer.lemmatize(w) for w in filtered_words]

    return " ".join(filtered_words)


def sentiment_polarity(text: str) -> str:
    """
    This function calculates the sentiment polarity of the text using TextBlob.
    """
    blob = TextBlob(text)
    return blob.sentiment.polarity


def categorize_sentiment(s: float, threshold=0.05) -> str:
    """
    This function categorizes the sentiment polarity into three categories: positive, negative, or neutral.
    Based on a given threshold, the default threshold is 0.05.
    """
    return "négatif" if s <= -threshold else "positif" if s >= threshold else "neutre"


def preprocess(df: pd.DataFrame) -> pd.DataFrame:

    # download the stopwords
    nltk.download('stopwords')
    stop_words = set(stopwords.words("english"))

    # drop the rows with missing values
    df = df.dropna()

    #  keep the columns that are needed
    COLUMNS_TO_KEEP = ["summary", "country", "city", "state", "date_time", "shape", "duration", "city_latitude","city_longitude"]
    df = df[COLUMNS_TO_KEEP]

    # Keep only the rows where the country is USA (and variations of USA)
    countries = ["USA", "usa", "USAv", "Usa", "USAUSA", "U", "Untied States of America"]
    df = df[df["country"].isin(countries)]
    df = df.drop("country", axis=1)

    # Cast the date_time column to a format dd-mm-yyyy hh:mm
    df["date_time"] = pd.to_datetime(df["date_time"], errors="coerce")

    # Convert the duration (string) to seconds (int)
    df["duration"] = df["duration"].apply(lambda x: convert_to_seconds(x))
    df = df.dropna(subset=["duration"])

    # Convert the shape to lowercase and keep only the primary shapes
    primary_shapes = ["light", "circle", "triangle", "fireball"]
    df["shape"] = df["shape"].apply(lambda x: x.lower())
    df["shape"] = df["shape"].apply(lambda x: x if x in primary_shapes else "other")

    # Sentiment analysis
    # Remove all stop words from the summary column
    lemmatizer = WordNetLemmatizer()
    df["summary"] = df["summary"].apply(preprocess_raw_text, stop_words=stop_words, lemmatizer=lemmatizer)
    df["sentiment"] = df["summary"].apply(sentiment_polarity)

    # Apply a threshold to the sentiment column, splitting it into three categories
    # [-1, -T] -> "negative"
    # (-T, +T) -> "neutral"
    # (+T, 1] -> "positive"
    df["sentiment"] = df["sentiment"].apply(lambda x: categorize_sentiment(x))

    # Save the processed CSV to assets/data
    if os.path.exists("assets/data/processed_data.csv"):
        os.remove("assets/data/processed_data.csv")

    df.to_csv("assets/data/processed_data.csv", quoting=csv.QUOTE_NONNUMERIC)
    print(">>> Data has been processed and saved to assets/data/processed_data.csv")

    return df


def convert_to_seconds(duration) -> float:
    """
    This function converts a duration string to seconds.

    Since the duration description are full of typos and inconsistencies, we need to preprocess the data before converting it to seconds.
    We first look for specific keywords (e.g. "s", "m", "h", "d", "w", "mo", "y") and then convert the duration to seconds. A manual inspection
    of was performed to identify the most common keywords and their corresponding values in seconds.

    In cases where, no duration could be extracted, the function returns None, which will be later dropped from the DataFrame.

    Overall this implementation successfully salvages >90% of the duration data.
    """

    # Convert the duration to lowercase and remove all non-alphanumeric characters
    duration = duration.lower()
    duration = "".join([c for c in duration if c.isalnum() or c.isspace() or c == "-"])

    # find if there is any number in the duration
    has_number = False

    for word in duration:
        if word.isnumeric():
            has_number = True
            break

    has_keyword = False

    for word in duration.split():
        if word in TIME_KEYWORDS:
            has_keyword = True
            break

    if has_keyword and has_number:
        duration_1 = [TIME_KEYWORDS.get(word, word) for word in duration.split()]

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
            word for word in duration_1 if word.isnumeric() or word in TIME_VALUES
        ]

        # print(f"{d_1:<20} -> {d_2:<20}")

        total_seconds = 0

        for i in range(len(duration_2) - 1):
            val_1 = duration_2[i]
            val_2 = duration_2[i + 1]

            if val_1.isnumeric() and val_2 in TIME_VALUES:

                if val_1 == "2½":
                    val_1 = 2
                total_seconds += int(val_1) * TIME_VALUES[val_2]

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

    # Keys : "Pre-1980" OR "1980" OR "1990" OR "2000" OR "2010" OR "Toutes"

    if decade == "Toutes":
        return df

    if decade == "Pre-1980":
        return df[df["date_time"].dt.year < 1980]

    min_year = int(decade)
    max_year = min_year + 9
    return df[
        (df["date_time"].dt.year >= min_year) & (df["date_time"].dt.year <= max_year)
    ]