import plotly.graph_objects as go
import plotly.express as px
import pandas as pd


state_centroids = {
    "AK": {"lat": 63.588753, "lon": -154.493062},
    "AL": {"lat": 32.318231, "lon": -86.902298},
    "AR": {"lat": 35.20105, "lon": -91.831833},
    "AZ": {"lat": 34.048928, "lon": -111.093731},
    "CA": {"lat": 36.778261, "lon": -119.417932},
    "CO": {"lat": 39.550051, "lon": -105.782067},
    "CT": {"lat": 41.603221, "lon": -73.087749},
    "DC": {"lat": 38.905985, "lon": -77.033418},
    "DE": {"lat": 38.910832, "lon": -75.52767},
    "FL": {"lat": 27.664827, "lon": -81.515754},
    "GA": {"lat": 32.157435, "lon": -82.907123},
    "HI": {"lat": 19.898682, "lon": -155.665857},
    "IA": {"lat": 41.878003, "lon": -93.097702},
    "ID": {"lat": 44.068202, "lon": -114.742041},
    "IL": {"lat": 40.633125, "lon": -89.398528},
    "IN": {"lat": 40.551217, "lon": -85.602364},
    "KS": {"lat": 39.011902, "lon": -98.484246},
    "KY": {"lat": 37.839333, "lon": -84.270018},
    "LA": {"lat": 31.244823, "lon": -92.145024},
    "MA": {"lat": 42.407211, "lon": -71.382437},
    "MD": {"lat": 39.045755, "lon": -76.641271},
    "ME": {"lat": 45.253783, "lon": -69.445469},
    "MI": {"lat": 44.314844, "lon": -85.602364},
    "MN": {"lat": 46.729553, "lon": -94.6859},
    "MO": {"lat": 37.964253, "lon": -91.831833},
    "MS": {"lat": 32.354668, "lon": -89.398528},
    "MT": {"lat": 46.879682, "lon": -110.362566},
    "NC": {"lat": 35.759573, "lon": -79.0193},
    "ND": {"lat": 47.551493, "lon": -101.002012},
    "NE": {"lat": 41.492537, "lon": -99.901813},
    "NH": {"lat": 43.193852, "lon": -71.572395},
    "NJ": {"lat": 40.058324, "lon": -74.405661},
    "NM": {"lat": 34.97273, "lon": -105.032363},
    "NV": {"lat": 38.80261, "lon": -116.419389},
    "NY": {"lat": 43.299428, "lon": -74.217933},
    "OH": {"lat": 40.417287, "lon": -82.907123},
    "OK": {"lat": 35.007752, "lon": -97.092877},
    "OR": {"lat": 43.804133, "lon": -120.554201},
    "PA": {"lat": 41.203322, "lon": -77.194525},
    "PR": {"lat": 18.220833, "lon": -66.590149},
    "RI": {"lat": 41.580095, "lon": -71.477429},
    "SC": {"lat": 33.836081, "lon": -81.163725},
    "SD": {"lat": 43.969515, "lon": -99.901813},
    "TN": {"lat": 35.517491, "lon": -86.580447},
    "TX": {"lat": 31.968599, "lon": -99.901813},
    "UT": {"lat": 39.32098, "lon": -111.093731},
    "VA": {"lat": 37.431573, "lon": -78.656894},
    "VT": {"lat": 44.558803, "lon": -72.577841},
    "WA": {"lat": 47.751074, "lon": -120.740139},
    "WI": {"lat": 43.78444, "lon": -88.787868},
    "WV": {"lat": 38.597626, "lon": -80.454903},
    "WY": {"lat": 43.075968, "lon": -107.290284},
}


def draw_map(df: pd.DataFrame, toggle_value: bool) -> go.Figure:

    df_by_city = (
        df.groupby(["city_longitude", "city_latitude", "city"])
        .size()
        .reset_index(name="count")
    )

    df_by_city.sort_values(by="count", ascending=False, inplace=True)

    if len(df_by_city) > 1500:
        df_by_city = df_by_city[0:1500]

    fig = go.Figure()

    if toggle_value:
        fig = px.scatter_mapbox(
            df_by_city,
            lat="city_latitude",
            lon="city_longitude",
            hover_name="city",
            size="count",
            color_discrete_sequence=["red"],
            zoom=3.5,
        )

        fig.update_layout(
            mapbox_style="white-bg",
            mapbox_layers=[
                {
                    "below": "traces",
                    "sourcetype": "raster",
                    "sourceattribution": "United States Geological Survey",
                    "source": [
                        "https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer/tile/{z}/{y}/{x}"
                    ],
                }
            ],
        )

    else:
        # Create a Scattergeo trace for the state initials
        state_initials_trace = go.Scattergeo(
            locationmode="USA-states",
            lon=[state_centroids[state]["lon"] for state in state_centroids],
            lat=[state_centroids[state]["lat"] for state in state_centroids],
            text=list(state_centroids.keys()),
            mode="text",
            textfont=dict(
                size=12,
                color="grey",
            ),
        )

        fig.add_trace(state_initials_trace)

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
            showlegend=False,
            geo=dict(
                scope="north america",
                landcolor="white",
                projection=dict(scale=3),
                center=dict(lat=40, lon=-100),
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

    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    fig.update_layout(
        mapbox_bounds={"west": -180, "east": -50, "south": 15, "north": 70}
    )

    return fig
