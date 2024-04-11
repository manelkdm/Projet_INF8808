from dash import Dash, html, dcc, callback, Output, Input
from dash_bootstrap_templates import load_figure_template
import dash_bootstrap_components as dbc
from components.filter_box import filter_box_layout
import preprocess

from components.map import draw_map
from components.cultural_events import draw_cultural_events_graph
from components.density_by_hour import draw_density_by_hour_graph
from components.duration import draw_duration_graph
from components.sentiment_analysis import draw_sentiment_analysis_graph
from components.heatmap import draw_heatmap_graph
from components.word_frequency import draw_word_frequency_graph

RUN_PREPROCESS = False

if RUN_PREPROCESS:
    raw_data = preprocess.load_raw_data()
    data = preprocess.preprocess(raw_data)
else:
    data = preprocess.load_data()

events_db = preprocess.load_events()

app = Dash(__name__, title="OVNI", external_stylesheets=[dbc.themes.LUX])
server = app.server
app._favicon = "images/ufo.png"
load_figure_template("LUX")

# HTML Layout
header = dbc.Container(
    [
        html.Img(src="assets/images/ufo.png", style={"height": "100px"}),
        html.H1("Observations d'OVNI au états-unis"),
        html.P("Simon Haché, Julien Milosz, Manel Keddam"),
    ],
    style={"textAlign": "center", "margin": "40px"},
)

filter_box = dbc.Container(
    filter_box_layout,
    style={
        "background-color": "DarkSeaGreen",
        "position": "-webkit-sticky",
        "position": "sticky",
        "top": "5px",
        "marginBottom": "50px",
        "padding": "20px",
        "width": "100%",
        "z-index": "2",
        "box-shadow": "5px 10px 5px Gainsboro",
    },
)

body = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                [
                    html.P("Carte des États-Unis", className="graph-title"),
                    dbc.Container(
                        dcc.Graph(
                            figure=draw_map(data),
                            id="map",
                            style={"height": "100%"},
                            config=dict(scrollZoom=False),
                        ),
                        style={"height": "1000px", "border": "1px solid black"},
                    ),
                ]
            )
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.P(
                            "Top 10 Mots Fréquemment Utilisés",
                            className="graph-title",
                        ),
                        dbc.Container(
                            dcc.Graph(
                                figure=draw_word_frequency_graph(data),
                                id="word_frequency",
                                style={"height": "100%"},
                            ),
                            style={"height": "500px", "border": "1px solid black"},
                        ),
                    ]
                ),
                dbc.Col(
                    [
                        html.P("Analyse de Sentiment", className="graph-title"),
                        dbc.Container(
                            dcc.Graph(
                                figure=draw_sentiment_analysis_graph(data),
                                id="sentiment",
                                style={"height": "100%"},
                            ),
                            style={"height": "500px", "border": "1px solid black"},
                        ),
                    ]
                ),
            ]
        ),
        dbc.Row(
            dbc.Col(
                [
                    html.P(
                        "Densité d'observations par jour",
                        className="graph-title",
                    ),
                    dbc.Container(
                        dcc.Graph(
                            figure=draw_heatmap_graph(data),
                            id="density_month",
                            style={"width": "100%"},
                        ),
                        style={"border": "1px solid black"},
                    ),
                ]
            )
        ),
        dbc.Row(
            dbc.Col(
                [
                    html.P(
                        "Densité d'observation par heure de la journée",
                        className="graph-title",
                    ),
                    dbc.Container(
                        dcc.Graph(
                            figure=draw_density_by_hour_graph(data),
                            id="density_hour",
                            style={"height": "100%"},
                        ),
                        style={"height": "500px", "border": "1px solid black"},
                    ),
                ]
            )
        ),
        dbc.Row(
            dbc.Col(
                [
                    html.P("Durée des observations", className="graph-title"),
                    dbc.Container(
                        dcc.Graph(
                            figure=draw_duration_graph(data),
                            id="duration",
                            style={"height": "100%"},
                        ),
                        style={"height": "500px", "border": "1px solid black"},
                    ),
                ]
            )
        ),
        dbc.Row(
            dbc.Col(
                [
                    html.P(
                        "Influence d'événements culturels marquants",
                        className="graph-title",
                    ),
                    dbc.Container(
                        dcc.Graph(
                            figure=draw_cultural_events_graph(data, events_db),
                            id="events",
                            style={"height": "100%"},
                        ),
                        style={"height": "500px", "border": "1px solid black"},
                    ),
                ]
            )
        ),
    ]
)

app.layout = dbc.Container([header, filter_box, body])


@app.callback(
    Output("map", "figure"),
    Output("word_frequency", "figure"),
    Output("sentiment", "figure"),
    Output("density_month", "figure"),
    Output("density_hour", "figure"),
    Output("duration", "figure"),
    Output("events", "figure"),
    Input("shape_filter", "value"),
    Input("duration_filter", "value"),
    Input("decade_filter", "value"),
)
def update_graphs(shape_filters: list[str], duration_filter: str, decade_filter: str):
    filtered_data = data.copy(deep=True)

    filtered_data = preprocess.filter_by_shapes(filtered_data, shape_filters)
    filtered_data = preprocess.filter_by_duration(filtered_data, duration_filter)
    filtered_data = preprocess.filter_by_decade(filtered_data, decade_filter)

    map = draw_map(filtered_data)
    word_frequency = draw_word_frequency_graph(filtered_data)
    sentiment = draw_sentiment_analysis_graph(filtered_data)
    density_month = draw_heatmap_graph(filtered_data)
    density_hour = draw_density_by_hour_graph(filtered_data)
    duration = draw_duration_graph(filtered_data)
    events = draw_cultural_events_graph(filtered_data, events_db)

    return (
        map,
        word_frequency,
        sentiment,
        density_month,
        density_hour,
        duration,
        events,
    )


if __name__ == "__main__":
    app.run(debug=True)
