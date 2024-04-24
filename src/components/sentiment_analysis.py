import plotly.graph_objects as go
import plotly.express as px

import pandas as pd


def draw_sentiment_analysis_graph(df) -> go.Figure:

    """
    This function draws a pie chart of the sentiment analysis of the text summary of the observations.
    
    There are 3 possible sentiments: "positif", "négatif", "neutre", pre-computed by the sentiment analysis preprocessing step.
    """

    sentiment_df = restructure_df(df)

    # Custom color map for the sentiment categories
    color_map = {
        "positif": "#8fbc8f",
        "négatif": "#bc8f8f",
        "neutre": "grey",
    }

    fig = px.pie(
        sentiment_df,
        names="sentiment",
        values="count",
        color="sentiment",
        color_discrete_map=color_map,
    )

    fig.update_traces(
        hovertemplate="<b>Sentiment:</b> %{label}<br><b>Nombre:</b> %{value:.0f}"
    )

    fig.add_annotation(
        x=1.05,
        y=1,
        text="Sentiment",
        showarrow=False,
        xref="paper",
        yref="paper",
        xanchor="left",
        yanchor="bottom",
        font=dict(size=14)
    )
    
    for data in fig.data:
        data.textfont.color = "white"
        data.textfont.size = 14
        data.marker.line.color = "white"
        data.marker.line.width = 1

    return fig


def restructure_df(df: pd.DataFrame) -> pd.DataFrame:

    sentiment_df = df.groupby("sentiment").size().reset_index(name="count")
    return sentiment_df
