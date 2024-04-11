from dash import html, dcc
import dash_bootstrap_components as dbc


shape_col = dbc.Container(
    [
        html.H3("Forme"),
        dbc.Container(
            dbc.Checklist(
                [
                    {"value": "light", "label": "Lumière"},
                    {"value": "circle", "label": "Cercle"},
                    {"value": "triangle", "label": "Triangle"},
                    {"value": "fireball", "label": "Boule de feu"},
                    {"value": "other", "label": "Autres"},
                ],
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
            [
                {"label": "Courte (< 1 minute)", "value": "short"},
                {"label": "Longue (> 1 minute)", "value": "long"},
                {"label": "Toutes", "value": "all"},
            ],
            "all",
            id="duration_filter",
        ),
    ]
)

decade_col = dbc.Container(
    [
        html.H3("Décennie"),
        dbc.Container(
            dbc.RadioItems(
                ["Pre-1980", "1980", "1990", "2000", "2010", "2020", "Toutes"],
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
