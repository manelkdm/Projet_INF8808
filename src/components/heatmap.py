import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# List of French month abbreviations
MONTHS_ABBREV_FR = [
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
        ]

# Start day of year for each month in a non-leap year
MONTHS_START_DAY = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]


def draw_heatmap_graph(df) -> go.Figure:

    """
    This function draws a heatmap of the number of observations by day of the year and year

    Each day of the year is represented by a square, and the color of the square represents the number of observations, in a gradient from light green to dark green

    """
    daily_density = restructure_df(df)

    # Custom color gradient with :
    # https://www.w3schools.com/colors/colors_picker.asp
    # Basecolor : # 8fbc8f
    fig = px.scatter(daily_density, x="day", y="year", color="counts", color_continuous_scale=["#dfecdf", "#305030"])

    # If a decade was selected in the filter
    if daily_density["year"].nunique() <= 10:
        fig.update_yaxes(tick0=1, dtick=1)

    fig.update_layout(
        xaxis_title_text="Jour de l'année",
        yaxis_title_text="Année",
        coloraxis_colorbar=dict(title="Nombre"),
    )

    fig.update_xaxes(
        tickmode="array",
        tickvals=MONTHS_START_DAY,
        ticktext=MONTHS_ABBREV_FR,
    )

    fig.update_traces(
        marker=dict(size=5, symbol="square"),
        hovertemplate="<b>Jour:</b> %{x}<br><b>Année:</b> %{y}<br><b>Nombre:</b> %{marker.color}",
        )
    return fig


def restructure_df(df: pd.DataFrame) -> pd.DataFrame:

    yearly_df = df.groupby([
        df['date_time'].dt.year.rename('year'),
        df['date_time'].dt.month.rename('month'),
        df['date_time'].dt.day_of_year.rename('day')
    ]).size().reset_index(name='counts')

    return yearly_df