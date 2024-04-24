import plotly.graph_objects as go
import pandas as pd
from collections import Counter
import plotly.express as px


def draw_word_frequency_graph(df: pd.DataFrame) -> go.Figure:

    """
    This function draws a horizontal bar graph of the top 10 most common words in the text summary of the observations.

    The words are counted after the NLP preprocessing step, which removes stopwords and punctuation, and aggregates the words using lemmatization.
    """

    top_words_df = restructure_df(df)

    fig = px.bar(top_words_df, x="Count", y="Word", orientation="h", color_discrete_sequence=["#8fbc8f"])

    fig.update_traces(
        hovertemplate="<b>Mot:</b> <i>%{y}</i><br><b>Nombre:</b> %{x:.0f}"
    )

    fig.update_yaxes(categoryorder="total ascending")

    fig.update_layout(
        xaxis_title_text="Nombre d'occurrences",
        yaxis_title_text="Mot",
    )

    return fig


def restructure_df(df: pd.DataFrame) -> pd.DataFrame:

    # Count the occurrences of each word in the summary
    all_words = " ".join(df["summary"]).lower().split()
    word_counts = Counter(all_words)

    # Get the top 10 most common words and their counts
    # Convert to DataFrame
    most_common_words = word_counts.most_common(10)
    top_words_df = pd.DataFrame(most_common_words, columns=["Word", "Count"])

    return top_words_df
