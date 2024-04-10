import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import matplotlib.colors as mcolors
import colorsys


def draw_heatmap_graph(df) -> go.Figure:  #
    """daily_density = restructure_df(df)"""
    daily_density = restructure_df(df)
    fig = px.scatter(daily_density, x="day", y="year", color="counts")

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

    amount_categories = {
        "nothing": (0, 0),
        "low": (1, 5),
        "medium": (6, 50),
        "high": (51, float("inf")),
    }

    yearly_df["category"] = yearly_df["counts"].apply(
        lambda x: get_category(x, amount_categories)
    )

    return yearly_df


def get_category(amount, amount_categories):
    for category, (min_amount, max_amount) in amount_categories.items():
        if min_amount <= amount <= max_amount:
            return category

    return "nothing"


def create_gradient_from_color(color, levels):
    hex_color = mcolors.hex2color(color)  # Convert hex to rgb
    hsv_color = colorsys.rgb_to_hsv(*hex_color)  # Convert rgb to hsv

    gradient = []
    for i in range(levels):
        lightness = i / levels
        rgb_color = colorsys.hsv_to_rgb(hsv_color[0], hsv_color[1], lightness)
        gradient.append(mcolors.rgb2hex(rgb_color))  # Convert rgb back to hex

    return gradient
