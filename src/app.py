from dash import Dash, html, dcc, callback, Output, Input
from dash_bootstrap_templates import load_figure_template
import dash_bootstrap_components as dbc
from components.filter_box import filter_box_layout

app = Dash(__name__, external_stylesheets=[dbc.themes.LUX])
load_figure_template("LUX")

# HTML Layout
header = dbc.Container(
    [
        html.H1("Observation d'OVNI au états-unis"),
        html.P("Simon Haché, Julien Milosz, Manel Keddam"),
    ],
    style={"textAlign": "center", "margin": "40px"},
)

filter_box = dbc.Container(
    filter_box_layout,
    style={
        "background-color": "lightgrey",
        "position": "-webkit-sticky",
        "position": "sticky",
        "top": "0",
        "margin-bottom": "50px",
        "padding": "20px",
        "width": "100%",
    },
)

body = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                [
                    html.P("Carte", className="graph-title"),
                    dbc.Container(
                        children=[],
                        style={"height": "500px", "border": "1px solid black"},
                    ),
                ]
            )
        ),  # Carte
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.P("Mots Fréquemments Utilisés", className="graph-title"),
                        dbc.Container(
                            children=[],
                            style={"height": "200px", "border": "1px solid black"},
                        ),
                    ]
                ),
                dbc.Col(
                    [
                        html.P("Analyse de Sentiment", className="graph-title"),
                        dbc.Container(
                            children=[],
                            style={"height": "200px", "border": "1px solid black"},
                        ),
                    ]
                ),
            ]
        ),
        dbc.Row(
            dbc.Col(
                [
                    html.P(
                        "Densité d'observations en fonction du mois",
                        className="graph-title",
                    ),
                    dbc.Container(
                        children=[],
                        style={"height": "1000px", "border": "1px solid black"},
                    ),
                ]
            )
        ),  # Densité d'observation par mois
        dbc.Row(
            dbc.Col(
                [
                    html.P(
                        "Densité d'observation par heure de la journée",
                        className="graph-title",
                    ),
                    dbc.Container(
                        children=[],
                        style={"height": "200px", "border": "1px solid black"},
                    ),
                ]
            )
        ),  # Densité d'observation par heure
        dbc.Row(
            dbc.Col(
                [
                    html.P("Durée des observations", className="graph-title"),
                    dbc.Container(
                        children=[],
                        style={"height": "200px", "border": "1px solid black"},
                    ),
                ]
            )
        ),  # Durée observations
        dbc.Row(
            dbc.Col(
                [
                    html.P(
                        "Influence d'événements culturels marquants",
                        className="graph-title",
                    ),
                    dbc.Container(
                        children=[],
                        style={"height": "200px", "border": "1px solid black"},
                    ),
                ]
            )
        ),  # Événements culturels
    ]
)


app.layout = dbc.Container([header, filter_box, body])


# Callbacks


if __name__ == "__main__":
    app.run(debug=True)
