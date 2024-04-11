import plotly.graph_objects as go
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

def draw_cultural_events_graph(df: pd.DataFrame, events_db: pd.DataFrame) -> go.Figure:

    cultural_events_df = restructure_df(df)

    # Convert date_time to string to be JSON serializable when plotting
    cultural_events_df["date_time"] = cultural_events_df["date_time"].astype(str)

    min_date = cultural_events_df["date_time"].min()
    max_date = cultural_events_df["date_time"].max()

    fig = px.line(cultural_events_df, x='date_time', y='count')

    fig.update_traces(
    line=dict(
        color="#8fbc8f",
        width=3
        )
    )

    fig.update_layout(
        xaxis_title_text="Date",
        yaxis_title_text="Nombre d'observations",
    )

    y_max = max(cultural_events_df["count"])
    fig.update_yaxes(range=[0, 1.2 * y_max ])

    # add a horzinotal line at the maximum value, red, width 2
    # fig.add_hline(y=y_max, line_dash="dot", line_color="red", line_width=2)

    event_category_colormap = {
        "Film/Série": "deepskyblue",
        "Mission Spatiale": "darkviolet",
        "Autres": "grey",
    }

    for i in range(len(events_db)):
        row = events_db.iloc[i]

        date_start = row["from"]
        date_end = row["to"]
        date_mid = get_mid_date(row)
        color = event_category_colormap[row["category"]]

        # Skip iteration if the date is out of the range
        if date_start < min_date or date_end > max_date:
            continue
        fig.add_vrect(
            x0=date_start, x1=date_end,
            fillcolor=color, opacity=0.5,
            layer="below", line_width=0,
        )

        # TODO : solve this properly
        # text_length = len(row["name"])
        y_coord = 0.9 * y_max

        # Pad the text with spaces to make it appear at the right position
        text_str = row["name"].rjust(30)

        #print(f"New text: {text_str}")
        # print(f"Text length: {text_length:<4}, y_max: {y_max:<4}, y_coord: {y_coord:<4}")

        fig.add_annotation(
            x=date_mid, y=y_coord,
            xref="x", yref="y",
            text=text_str,
            showarrow=False,
            font=dict(size=12),
            textangle=-90,
            align="right",
        )

    # Add dummy traces for legend
    for category, color in event_category_colormap.items():
        fig.add_trace(go.Scatter(
            x=[None], y=[None],
            mode='markers',
            marker=dict(size=10, color=color),
            showlegend=True,
            name=category,
        ))

    return fig


def restructure_df(df: pd.DataFrame) -> pd.DataFrame:

    cultural_events_df = df.copy()
    cultural_events_df = cultural_events_df.groupby(cultural_events_df["date_time"].dt.to_period("M")).size().reset_index(name='count')

    return cultural_events_df


def get_mid_date(row) -> datetime:
    date_format = "%Y-%m-%d"

    date_start = datetime.strptime(row["from"], date_format)
    date_end = datetime.strptime(row["to"], date_format)

    date_mid = date_start + (date_end - date_start) / 2


    return date_mid