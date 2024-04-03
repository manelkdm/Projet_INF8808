from dash import html, dcc
import dash_bootstrap_components as dbc


shape_col = dbc.Container(
    [
        html.H3("Forme"),
        dbc.Container(
            dbc.Checklist(
                ["Lumière", "Cercle", "Triangle", "Boule de feu", "Autres"],
                [],
                id="shape_filter",
            ),
        ),
    ]
)

duration_col = dbc.Container(
    [
        html.H3("Durée"),
        dbc.RadioItems(
            ["Courte (< 1 minute)", "Longue (> 1 minute)", "Toutes"],
            "Toutes",
            id="duration_filter",
        ),
    ]
)

decade_col = dbc.Container(
    [
        html.H3("Décennie"),
        dbc.Container(
            dbc.RadioItems(
                ["1990", "2000", "2010", "2020", "Toutes"],
                "Toutes",
                id="decade_filter",
            ),
        ),
    ]
)

filter_box_layout = html.Div(
    dbc.Row(
        [
            dbc.Col(shape_col),
            dbc.Col(duration_col),
            dbc.Col(decade_col),
        ]
    )
)
