import plotly.graph_objects as go
import plotly.express as px

import pandas as pd


def draw_sentiment_analysis_graph(df) -> go.Figure:

    sentiment_df = restructure_df(df)

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

    return fig


def restructure_df(df: pd.DataFrame) -> pd.DataFrame:

    sentiment_df = df.groupby("sentiment").size().reset_index(name="count")

    return sentiment_df
