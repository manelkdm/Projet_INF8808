import plotly.graph_objects as go
import pandas as pd
import plotly.express as px


def draw_cultural_events_graph(df) -> go.Figure:

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

    events_db = pd.read_csv("./assets/data/events.csv")

    color_map = {
        "Movie": "lightblue",
        "Space": "lightgreen",
        "Other": "lightcoral",
    }

    for i in range(len(events_db)):
        row = events_db.iloc[i]

        # Skip iteration if the date is out of the range
        if row["from"] < min_date or row["to"] > max_date:
            continue
        fig.add_vrect(
            x0=row["from"], x1=row["to"],
            fillcolor=color_map[row["category"]], opacity=0.5,
            layer="below", line_width=0,
        )

        # TODO : solve this properly
        # fig.add_annotation(
        #     x=row["from"], y=0,
        #     xref="x", yref="paper",
        #     text=row["category"],
        #     showarrow=False,
        #     font=dict(size=12),
        # )

    # Add dummy traces for legend
    for category, color in color_map.items():
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
