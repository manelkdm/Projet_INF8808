from dash import html
import dash_bootstrap_components as dbc


shape_col = dbc.Container(
    [
        dbc.Textarea("Forme"),
        dbc.ListGroup(
            [
                dbc.Col(
                    dbc.ListGroupItem(
                        [
                            dbc.Checkbox(id="light_shape_filter"),
                            dbc.Textarea("Lumière"),
                        ]
                    ),
                    dbc.ListGroupItem(
                        [
                            dbc.Checkbox(id="circle_shape_filter"),
                            dbc.Textarea("Cercle"),
                        ]
                    ),
                    dbc.ListGroupItem(
                        [
                            dbc.Checkbox(id="triangle_shape_filter"),
                            dbc.Textarea("Triangle"),
                        ]
                    ),
                ),
                dbc.Col(
                    dbc.ListGroupItem(
                        [
                            dbc.Checkbox(id="fireball_shape_filter"),
                            dbc.Textarea("Boule de feu"),
                        ]
                    ),
                    dbc.ListGroupItem(
                        [
                            dbc.Checkbox(id="others_shape_filter"),
                            dbc.Textarea("Autres"),
                        ]
                    ),
                ),
            ]
        ),
    ]
)

duration_col = dbc.Container(
    [
        dbc.Textarea("Durée"),
        dbc.ListGroup(
            [
                dbc.ListGroupItem(
                    [
                        dbc.RadioButton(id="low_duration_filter"),
                        dbc.Textarea("Courte (< 1 minute)"),
                    ]
                ),
                dbc.ListGroupItem(
                    [
                        dbc.RadioButton(id="long_duration_filter"),
                        dbc.Textarea("Longue (> 1 minute)"),
                    ]
                ),
                dbc.ListGroupItem(
                    [
                        dbc.RadioButton(id="all_duration_filter"),
                        dbc.Textarea("Toutes"),
                    ]
                ),
            ]
        ),
    ]
)

decade_col = dbc.Container(
    [
        dbc.Textarea("Décennie"),
        dbc.ListGroup(
            [
                dbc.Col(
                    dbc.ListGroupItem(
                        [
                            dbc.Checkbox(id="90s_filter"),
                            dbc.Textarea("1990"),
                        ]
                    ),
                    dbc.ListGroupItem(
                        [
                            dbc.Checkbox(id="00s_filter"),
                            dbc.Textarea("2000"),
                        ]
                    ),
                    dbc.ListGroupItem(
                        [
                            dbc.Checkbox(id="10s_filter"),
                            dbc.Textarea("2010"),
                        ]
                    ),
                ),
                dbc.Col(
                    dbc.ListGroupItem(
                        [
                            dbc.Checkbox(id="20s_filter"),
                            dbc.Textarea("2020"),
                        ]
                    ),
                    dbc.ListGroupItem(
                        [
                            dbc.Checkbox(id="all_decades_filter"),
                            dbc.Textarea("Toutes"),
                        ]
                    ),
                ),
            ]
        ),
    ]
)

filter_box_layout = html.div(
    dbc.Container(
        [
            dbc.Col(shape_col),
            dbc.Col(duration_col),
            dbc.Col(decade_col),
        ]
    )
)
