import plotly.graph_objects as go
import plotly.express as px
import pandas as pd


def draw_duration_graph(df: pd.DataFrame) -> go.Figure:

    duration_df = restructure_df(df)

    fig = px.histogram(
        duration_df,
        x="duration",
        nbins=50,
        color_discrete_sequence=["#8fbc8f"],
    )

    max_duration = int(duration_df["duration"].max())
    tick_values = list(range(0, max_duration + 1, 60))

    fig.update_layout(
        xaxis_title_text="Durées (secondes)",
        yaxis_title_text="Nombre d'observations",
        xaxis=dict(tickmode="array", tickvals=tick_values),
    )

    return fig


def restructure_df(df: pd.DataFrame) -> pd.DataFrame:

    duration_df = df.copy()
    duration_df = duration_df[["duration"]]

    # TODO: remove this at the end
    # find the 10% and 90% quantile
    # q10 = duration_df["duration"].quantile(0.1)
    # q90 = duration_df["duration"].quantile(0.9)

    # print("-" * 100)
    # print(f"10% quantile: {q10} - 90% quantile: {q90}")
    # print("-" * 100)

    # drop all duration > 2000
    duration_df = duration_df[duration_df["duration"] < 2000]

    return duration_df
