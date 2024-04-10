import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import matplotlib.colors as mcolors
import colorsys

def draw_heatmap_graph(df) -> go.Figure:

    monthly_density = restructure_df(df)

    gradient = create_gradient_from_color("#8fbc8f", 10)

    fig = px.imshow(monthly_density, color_continuous_scale=gradient)

    fig.update_layout(
        xaxis=dict(
            title="Mois",
            tickmode="array",
            tickvals=list(range(1, 13)),
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
        ),
        yaxis=dict(title="Année"),
    )

    return fig


def restructure_df(df: pd.DataFrame) -> pd.DataFrame:

    # Create a deep copy of the df called yearly_df
    yearly_df = df.copy()

    # Create a new column called "year" that contains the year of the date_time column
    yearly_df["year"] = yearly_df["date_time"].dt.year
    yearly_df["month"] = yearly_df["date_time"].dt.month

    # drop all columns except "year" and "month"
    yearly_df = yearly_df[["year", "month"]]
    yearly_df = yearly_df.groupby(["year", "month"]).size().reset_index(name="counts")

    # Create a new df with rows = year, columns = month, values = count of observations
    yearly_df = yearly_df.pivot(index="year", columns="month", values="counts")
    yearly_df = yearly_df.fillna(0).astype(int)

    return yearly_df


def create_gradient_from_color(color, levels):
    hex_color = mcolors.hex2color(color)  # Convert hex to rgb
    hsv_color = colorsys.rgb_to_hsv(*hex_color)  # Convert rgb to hsv

    gradient = []
    for i in range(levels):
        lightness = (i / levels)
        rgb_color = colorsys.hsv_to_rgb(hsv_color[0], hsv_color[1], lightness)
        gradient.append(mcolors.rgb2hex(rgb_color))  # Convert rgb back to hex

    return gradient