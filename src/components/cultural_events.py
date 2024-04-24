import plotly.graph_objects as go
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

def draw_cultural_events_graph(df: pd.DataFrame, events_db: pd.DataFrame) -> go.Figure:
    """
    This function draws a line graph of the number of observations over time
    with vertical rectangles representing cultural events colored by their given category (Film/Série, Mission Spatiale, Autres)

    Each cultural event is represented by a vertical rectangle spanning from the start date to the end date, representing the duration of influence of the event.
    For example, movies where usually given a -2/+2 months of influence to account for the pre-release and post-release period. Same for space missions.

    Unsual events are also represented, such as the release of classified documents, or the discovery of a new exoplanet. These events have an influence period starting from the date of the event,
    since they cannot be predicted in advance, in contrast to movies or space missions.
    """

    cultural_events_df = restructure_df(df)

    min_year = df['date_time'].dt.year.min()
    max_year = df['date_time'].dt.year.max()

    year_range = max_year - min_year
    # print(f"Year range: {year_range}")

    # Convert date_time to string to be JSON serializable when plotting
    cultural_events_df["date_time"] = cultural_events_df["date_time"].astype(str)

    min_date = cultural_events_df["date_time"].min()
    max_date = cultural_events_df["date_time"].max()

    fig = px.line(cultural_events_df, x='date_time', y='count')

    fig.update_traces(
        line=dict(
            color="#8fbc8f",
            width=3
            ),
        hovertemplate="<b>Date:</b> %{x}<br><b>Nombre:</b> %{y:.0f}"
    )

    fig.update_layout(
        xaxis_title_text="Date",
        yaxis_title_text="Nombre d'observations",
    )

    y_max = max(cultural_events_df["count"])
    fig.update_yaxes(range=[0, 1.2 * y_max ])


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
        y_coord = 0.9 * y_max

        # Pad the text with spaces to make it appear at the right position
        text_str = row["name"].rjust(30)

        # TODO: play with the tick values to make it more readable
        # if year_range < 3: # 2020 - 2023 : tick every 3 months
        #     fig.update_xaxes(dtick="M3", tickformat="%b %Y")
        # elif year_range < 10: # Decade : tick every 1 year
        #     fig.update_xaxes(dtick="M12", tickformat="%Y")
        # else: # All : tick every 3 years
        #     # TODO : tick every 3 years not possible in Plotly ...
        #     pass
        #     # fig.update_xaxes(dtick="M12", tickformat="%Y")

        fig.update_xaxes(tickangle=90)

        fig.add_annotation(
            x=date_mid, y=y_coord,
            xref="x", yref="y",
            text=text_str,
            showarrow=False,
            font=dict(size=12, color="black"),
            textangle=90,
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

    cultural_events_df = df.groupby(df["date_time"].dt.to_period("M")).size().reset_index(name='count')
    return cultural_events_df


def get_mid_date(row) -> datetime:
    date_format = "%Y-%m-%d"

    date_start = datetime.strptime(row["from"], date_format)
    date_end = datetime.strptime(row["to"], date_format)

    date_mid = date_start + (date_end - date_start) / 2

    return date_mid