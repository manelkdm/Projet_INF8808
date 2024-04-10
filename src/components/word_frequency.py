import plotly.graph_objects as go
import pandas as pd
from collections import Counter
import plotly.express as px


def draw_word_frequency_graph(df: pd.DataFrame) -> go.Figure:

    top_words_df = restructure_df(df)

    fig = px.bar(top_words_df, x="Count", y="Word", orientation="h")
    fig.update_yaxes(categoryorder="total ascending")

    return fig


def restructure_df(df: pd.DataFrame) -> pd.DataFrame:

    all_words = " ".join(df["summary"]).lower().split()
    word_counts = Counter(all_words)

    # Get the top 10 most common words and their counts
    most_common_words = word_counts.most_common(10)

    # Convert to DataFrame
    top_words_df = pd.DataFrame(most_common_words, columns=["Word", "Count"])

    return top_words_df
