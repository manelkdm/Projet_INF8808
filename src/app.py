from dash import Dash, html, dcc, callback, Output, Input
from dash_bootstrap_templates import load_figure_template
import dash_bootstrap_components as dbc
from components.filter_box import filter_box_layout

app = Dash(__name__, external_stylesheets=[dbc.themes.LUX])
load_figure_template("LUX")

# HTML Layout
header = html.div(
    [
        html.H1("Observation d'OVNI au états-unis"),
        html.p("Simon Haché, Julien Milosz, Manel Keddam"),
        filter_box_layout,
    ]
)

body = html.div(
    [
        dbc.Row(dbc.Col()),  # Carte
        dbc.Row([dbc.Col(), dbc.Col()]),  # Mots fréquents + sentiment analysis
        dbc.Row(dbc.Col()),  # Densité d'observation par mois
        dbc.Row(dbc.Col()),  # Densité d'observation par heure
        dbc.Row(dbc.Col()),  # Durée observations
        dbc.Row(dbc.Col()),  # Événements culturels
    ]
)


app.layout = html.div([header, body])


# Callbacks


@callback(Output("graph-content", "figure"), Input("", "value"))
def update_graph(value):
    pass


if __name__ == "__main__":
    app.run(debug=True)
