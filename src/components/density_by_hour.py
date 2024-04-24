import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np


def draw_density_by_hour_graph(df) -> go.Figure:
    """
    This function draws a polar bar graph of the number of observations by hour of the day on a 24-hour clock
    Since the data is from 0 to 23, each value gets myltiplied by 15 to get the angle in degrees (0 to 360).
    
    Midnight is at the 90° angle, and the graph is drawn clockwise.

    The radius "r" can be any of the following: "frequency", "log_frequency", "sqrt_frequency" to represent the data differently.
    """

    df = restructure_df(df)

    fig = px.bar_polar(
        df,
        r="frequency",
        theta="angle",
        color_discrete_sequence=["#8fbc8f"],
        direction="clockwise",
        start_angle=90,
    )

    fig.update_traces(
        hovertemplate="<b>Heure:</b> %{theta}h<br><b>Nombre:</b> %{r}"
    )

    fig.update_layout(
        polar=dict(
            angularaxis=dict(
                tickmode="array",
                tickvals=np.arange(24) * 15,
                ticktext=[str(i) for i in range(24)],
            ),
            # Radial axis (radius = frequency)
            radialaxis=dict(
                title = dict(text="Nombre", font=dict(size=14)),
                tickangle=90,
            ),
        )
    )

    # Custom annotation for the angular axis (angle = hour)
    fig.add_annotation(
        text="Heure de la journée",
        x=0.5,
        y=1.15,
        showarrow=False,
        font=dict(size=14),
        xref="paper",
        yref="paper",
    )

    return fig


def restructure_df(df: pd.DataFrame) -> pd.DataFrame:

    ANGLE_PER_HOUR = 360 / 24

    # Deep copy only the date_time column
    hourly_df = df[['date_time']].copy(deep=True)
    hourly_df["hour"] = hourly_df["date_time"].dt.hour

    # Drop all columns except "hour", add a column "frequency" that counts the number of observations for each hour
    hourly_df = hourly_df[["hour"]]
    hourly_df = hourly_df.groupby(["hour"]).size().reset_index(name="frequency")
    hourly_df["angle"] = hourly_df["hour"] * ANGLE_PER_HOUR

    # Add a transformed frequency column : log_frequency and sqrt_frequency
    hourly_df["log_frequency"] = np.log(hourly_df["frequency"])
    hourly_df["sqrt_frequency"] = np.sqrt(hourly_df["frequency"])

    return hourly_df

