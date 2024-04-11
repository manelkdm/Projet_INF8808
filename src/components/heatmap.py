import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import matplotlib.colors as mcolors
import colorsys


def draw_heatmap_graph(df) -> go.Figure:  #
    """daily_density = restructure_df(df)"""
    daily_density = restructure_df(df)

    # Custom color gradient with :
    # https://www.w3schools.com/colors/colors_picker.asp
    # Basecolor : # 8fbc8f
    fig = px.scatter(daily_density, x="day", y="year", color="counts", color_continuous_scale=["#dfecdf", "#305030"])

    if daily_density["year"].nunique() <= 10:
        fig.update_yaxes(tick0=1, dtick=1)

    fig.update_layout(
        xaxis_title_text="Jour de l'année",
        yaxis_title_text="Année",
        coloraxis_colorbar=dict(title="Nombre"),
    )

    fig.update_xaxes(
        tickmode="array",
        tickvals=[0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334],
        ticktext=[
            "Jan",
            "Fév",
            "Mar",
            "Avr",
            "Mai",
            "Jun",
            "Jul",
            "Aoû",
            "Sep",
            "Oct",
            "Nov",
            "Déc",
        ],
    )

    fig.update_traces(marker=dict(size=5, symbol="square"))
    return fig


def restructure_df(df: pd.DataFrame) -> pd.DataFrame:

    # Create a deep copy of the df called yearly_df
    yearly_df = df.copy()

    # Create a new column called "year" that contains the year of the date_time column
    yearly_df["year"] = yearly_df["date_time"].dt.year
    yearly_df["month"] = yearly_df["date_time"].dt.month
    yearly_df["day"] = yearly_df["date_time"].dt.day_of_year

    # drop all columns except "year" and "month"
    yearly_df = yearly_df[["year", "month", "day"]]
    yearly_df = (
        yearly_df.groupby(["year", "month", "day"]).size().reset_index(name="counts")
    )

    # Create a new column called "category" that contains the category of the counts
    # bins = [0, 1, 6, 51, float('inf')]
    # labels = ['nothing', 'low', 'medium', 'high']
    # yearly_df['category'] = pd.cut(yearly_df['counts'], bins=bins, labels=labels)

    return yearly_df