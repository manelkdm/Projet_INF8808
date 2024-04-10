import plotly.graph_objects as go
import pandas as pd


def draw_map(df: pd.DataFrame) -> go.Figure:

    df_by_city = (
        df.groupby(["city_longitude", "city_latitude", "city"])
        .size()
        .reset_index(name="count")
    )

    df_by_city.sort_values(by="count", ascending=False, inplace=True)

    df_by_city = df_by_city[0:3000]

    fig = go.Figure()

    fig.add_trace(
        go.Scattergeo(
            locationmode="USA-states",
            lon=df_by_city["city_longitude"],
            lat=df_by_city["city_latitude"],
            text=df_by_city["city"],
            mode="markers",
            marker=dict(
                size=df_by_city["count"] * 1.5,
                color="ForestGreen",
                sizemode="area",
            ),
        )
    )

    fig.update_layout(
        title_text="2014 US city populations",
        showlegend=False,
        geo=dict(
            scope="usa",
            landcolor="white",
        ),
    )

    fig.update_geos(
        resolution=50,
        showlakes=True,
        lakecolor="LightBlue",
        showrivers=True,
        rivercolor="LightBlue",
        showland=True,
        landcolor="FloralWhite",
        subunitcolor="Black",
    )

    return fig
