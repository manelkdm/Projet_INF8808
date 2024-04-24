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
        tickvals=[0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334], # Starting day of the year for each month
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

    yearly_df = df.groupby([
        df['date_time'].dt.year.rename('year'),
        df['date_time'].dt.month.rename('month'),
        df['date_time'].dt.day_of_year.rename('day')
    ]).size().reset_index(name='counts')

    return yearly_df