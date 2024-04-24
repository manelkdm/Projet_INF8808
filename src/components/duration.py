import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np


def draw_duration_graph(df: pd.DataFrame) -> go.Figure:
    """
    This function draws a histogram of the duration of the observations with a logarithmic scale (base 2) on the x-axis (seconds)
    Custom tick values are used to represent common time intervals (e.g. 1 sec, 10 sec, 30 sec, 1 min, 5 min, ...)
    """

    duration_df = restructure_df(df)

    # LOG DURATION
    fig = px.histogram(
        duration_df,
        x="log_duration",
        nbins=50,
        color_discrete_sequence=["#8fbc8f"],
    )

    # Create custom tick values for the x-axis
    second_vales = [1, 10, 30, 60, 5*60, 10*60, 30*60, 60*60, 24*60*60, 7*24*60*60, 30*24*60*60, 365*24*60*60]
    tick_values = [np.log2(x) for x in second_vales]
    tick_text = ["1 sec", "10 sec", "30 sec", "1 min", "5 min", "10 min", "30 min", "1 heure", "1 jour", "1 sem", "1 mois", "1 année"]

    fig.update_layout(
        xaxis_title_text="Log durée",
        yaxis_title_text="Nombre d'observations",
        xaxis=dict(tickmode="array", tickvals=tick_values),
    )

    fig.update_xaxes(
        tickmode="array",
        tickvals=tick_values,
        ticktext=tick_text
    )

    return fig


def restructure_df(df: pd.DataFrame) -> pd.DataFrame:

    # Deep copy the duration column and apply a log2 transformation
    duration_df = df[["duration"]].copy(deep=True)
    duration_df["log_duration"] = duration_df["duration"].apply(lambda x: np.log2(x))

    return duration_df
