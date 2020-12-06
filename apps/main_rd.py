# import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

# import dash_table

import plotly.graph_objs as go

import numpy as np

import rd_functions.main_functions as mf

# import rd_functions.util_mod as um
# import rd_functions.prob_weighting as pw
import rd_functions.custom_exceptions as ce

import apps.func_dicts as fd

plot_color = fd.plot_color
prim_color = fd.prim_color

header_style = {"background-color": prim_color}
header_class = "my-2 p-2 text-white rounded"

heat_scale = fd.heat_scale
from math import isclose, nan

from app import app


gl_segment = dbc.Collapse(
    [
        html.H3(
            html.Strong(
                [html.Span("Gain Loss Utility function - "), html.Span(id="gl_heading")]
            ),
            style=header_style,
            className=header_class,
        ),
        html.Div(
            [
                html.Div(
                    [
                        dcc.Dropdown(
                            id="gl_dropdown",
                            options=[
                                {
                                    "label": "Tversky Kahneman utility function",
                                    "value": "TKU",
                                },
                                {"label": "Linear Utility function", "value": "LU",},
                                {"label": "Root utility function", "value": "RU",},
                                {
                                    "label": "Exponential utiltiy function",
                                    "value": "EXU",
                                },
                                {"label": "Bernoulli utility function", "value": "BU",},
                                {"label": "Your utility function", "value": "YU",},
                            ],
                            value="TKU",
                            className="py-2 d-print-none",
                        ),
                        dbc.Collapse(
                            [
                                dbc.Label("Your utility function:"),
                                # MARK Textarea for ASTEVAL
                                dbc.Input(
                                    id="gl_text",
                                    type="text",
                                    placeholder="Input your own function",
                                    debounce=True,
                                ),
                                dbc.Button(
                                    "Run Function",
                                    id="gl_text_runner",
                                    className="mt-2",
                                ),
                            ],
                            id="gl_collapse_YU",
                            className="py-2",
                        ),
                        dbc.Collapse(
                            [
                                dbc.Label("Formula:"),
                                html.Div(fd.um_func_dict["TKU"][2], className="pb-2"),
                                dbc.FormGroup(
                                    [
                                        dbc.Label("a:", width=3, className="my-1",),
                                        dbc.Col(
                                            dbc.Input(
                                                id="gl_TKU_a",
                                                type="number",
                                                value=0.88,
                                                step=0.1,
                                            ),
                                            width=9,
                                        ),
                                        dbc.Label("l:", width=3, className="my-1",),
                                        dbc.Col(
                                            dbc.Input(
                                                id="gl_TKU_l",
                                                type="number",
                                                value=2.25,
                                                step=0.1,
                                            ),
                                            width=9,
                                        ),
                                        dbc.Label("r:", width=3, className="my-1",),
                                        dbc.Col(
                                            dbc.Input(
                                                id="gl_TKU_r",
                                                type="number",
                                                value=0.0,
                                                step=1,
                                            ),
                                            width=9,
                                        ),
                                    ],
                                    row=True,
                                ),
                            ],
                            id="gl_collapse_TKU",
                            className="py-2",
                        ),
                        dbc.Collapse(
                            [
                                dbc.Label("Formula:"),
                                html.Div(fd.um_func_dict["RU"][2], className="pb-2"),
                                dbc.FormGroup(
                                    [
                                        dbc.Label("exp:", width=3, className="my-1",),
                                        dbc.Col(
                                            dbc.Input(
                                                id="gl_RU_exp",
                                                type="number",
                                                value=2.0,
                                                step=1,
                                            ),
                                            width=9,
                                        ),
                                    ],
                                    row=True,
                                ),
                            ],
                            id="gl_collapse_RU",
                            className="py-2",
                        ),
                        dbc.Collapse(
                            [
                                dbc.Label("Formula:"),
                                html.Div(fd.um_func_dict["EXU"][2], className="pb-2"),
                                dbc.FormGroup(
                                    [
                                        dbc.Label("a:", width=3, className="my-1",),
                                        dbc.Col(
                                            dbc.Input(
                                                id="gl_EXU_a",
                                                type="number",
                                                value=1.0,
                                                step=0.01,
                                            ),
                                            width=9,
                                        ),
                                    ],
                                    row=True,
                                ),
                            ],
                            id="gl_collapse_EXU",
                            className="py-2",
                        ),
                        dbc.Collapse(
                            [
                                dbc.Label("Formula:"),
                                html.Div(fd.um_func_dict["BU"][2], className="pb-2"),
                                dbc.FormGroup(
                                    [
                                        dbc.Label("a:", width=3, className="my-1",),
                                        dbc.Col(
                                            dbc.Input(
                                                id="gl_BU_a",
                                                type="number",
                                                value=0.0,
                                                step=0.01,
                                            ),
                                            width=9,
                                        ),
                                    ],
                                    row=True,
                                ),
                            ],
                            id="gl_collapse_BU",
                            className="py-2",
                        ),
                        dbc.Collapse(
                            [
                                dbc.Label("Formula:"),
                                html.Div(fd.um_func_dict["LU"][2], className="pb-2"),
                            ],
                            id="gl_collapse_LU",
                            className="py-2",
                        ),
                        dbc.Button(
                            "Reset all values",
                            id="gl_reset_btn",
                            className="my-3 d-print-none",
                        ),
                    ],
                    className="col",
                ),
                html.Div(
                    [
                        dcc.Graph(id="gl_graph"),
                        dbc.FormGroup(
                            [
                                dbc.Label(
                                    "Minimum display value:", width=3, className="my-1",
                                ),
                                dbc.Col(
                                    dbc.Input(
                                        id="gl_min_value", type="number", value=0,
                                    ),
                                    width=3,
                                ),
                                dbc.Label(
                                    "Maximum display value:", width=3, className="my-1",
                                ),
                                dbc.Col(
                                    dbc.Input(
                                        id="gl_max_value", type="number", value=10,
                                    ),
                                    width=3,
                                ),
                            ],
                            row=True,
                            className="my-2 d-print-none",
                        ),
                    ],
                    className="col-8",
                ),
            ],
            className="row mt-2",
        ),
    ],
    id="gl_panel_collapse",
)


@app.callback(
    [
        Output("gl_TKU_a", "value"),
        Output("gl_TKU_l", "value"),
        Output("gl_TKU_r", "value"),
        Output("gl_RU_exp", "value"),
        Output("gl_EXU_a", "value"),
        Output("gl_BU_a", "value"),
        Output("gl_min_value", "value"),
        Output("gl_max_value", "value"),
    ],
    [Input("gl_reset_btn", "n_clicks")],
)
def gl_reset(n_clicks):
    # Reset all parameters for the utility function
    return (
        0.88,
        2.25,
        0,
        2,
        1,
        0,
        0,
        10,
    )


@app.callback(
    [
        Output("gl_collapse_TKU", "is_open"),
        Output("gl_collapse_RU", "is_open"),
        Output("gl_collapse_LU", "is_open"),
        Output("gl_collapse_BU", "is_open"),
        Output("gl_collapse_EXU", "is_open"),
        Output("gl_collapse_YU", "is_open"),
    ],
    [Input("gl_dropdown", "value")],
    [
        State("gl_collapse_TKU", "is_open"),
        State("gl_collapse_RU", "is_open"),
        State("gl_collapse_LU", "is_open"),
        State("gl_collapse_BU", "is_open"),
        State("gl_collapse_EXU", "is_open"),
        State("gl_collapse_YU", "is_open"),
    ],
)
def toggle_gl_params(
    drop_val, TKU_open, RU_open, LU_open, BU_open, EXU_open, YU_open,
):
    (TKU_open, RU_open, LU_open, BU_open, EXU_open, YU_open,) = (
        False,
        False,
        False,
        False,
        False,
        False,
    )
    if drop_val == "TKU":
        TKU_open = True
    elif drop_val == "RU":
        RU_open = True
    elif drop_val == "LU":
        LU_open = True
    elif drop_val == "BU":
        BU_open = True
    elif drop_val == "EXU":
        EXU_open = True
    elif drop_val == "YU":
        YU_open = True
    return (
        TKU_open,
        RU_open,
        LU_open,
        BU_open,
        EXU_open,
        YU_open,
    )


@app.callback(
    [
        Output("gl_graph", "figure"),
        Output("danger_toast_5", "children"),
        Output("danger_toast_5", "is_open"),
    ],
    [
        Input("gl_dropdown", "value"),
        Input("gl_min_value", "value"),
        Input("gl_max_value", "value"),
        Input("gl_TKU_a", "value"),
        Input("gl_TKU_l", "value"),
        Input("gl_TKU_r", "value"),
        Input("gl_RU_exp", "value"),
        Input("gl_BU_a", "value"),
        Input("gl_EXU_a", "value"),
        Input("gl_text_runner", "n_clicks"),
        Input("gl_text", "value"),
    ],
)
def update_gl_graph(
    gl_drop_val,
    min_val,
    max_val,
    TKU_a,
    TKU_l,
    TKU_r,
    RU_exp,
    BU_a,
    EXU_a,
    n_clicks,
    user_func,
):
    if gl_drop_val == "TKU":
        kwargs = {"a": TKU_a, "l": TKU_l, "r": TKU_r}
    elif gl_drop_val == "RU":
        kwargs = {"exp": RU_exp}
    elif gl_drop_val == "LU":
        kwargs = {}
    elif gl_drop_val == "BU":
        kwargs = {"a": BU_a}
    elif gl_drop_val == "EXU":
        kwargs = {"a": EXU_a}
    elif gl_drop_val == "YU":
        kwargs = {"text": user_func}

    x_1_data = np.linspace(min_val, max_val, 100)
    # y_1_data = [fd.gl_func_dict[gl_drop_val][0](float(i), **kwargs) for i in x_1_data]

    danger_text = ""
    danger_bool = False
    y_1_data = []

    for i in x_1_data:
        try:
            y_1_data.append(fd.um_func_dict[gl_drop_val][0](float(i), **kwargs))
        except ce.PositiveValuesOnlyError:
            y_1_data.append(nan)
            danger_text = (
                "The utility function you chose doesn't process negative values"
            )
            danger_bool = True

    fig = go.Figure(
        data=[
            go.Scatter(
                x=x_1_data,
                y=y_1_data,
                line=dict(color=plot_color, width=4,),
                marker=dict(color=plot_color),
            )
        ]
    )
    fig.update_layout(
        template="plotly_white",
        margin=dict(l=25, r=25, b=25, t=25, pad=0),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        # title="Utility function",
        xaxis_title="Payoff",
        yaxis_title="Utility",
        height=300,
    )
    fig.update_xaxes(
        showgrid=False,
        # zeroline=False
    )
    fig.update_yaxes(showgrid=False)

    return fig, danger_text, danger_bool


um_segment = html.Div(
    [
        html.H3(
            html.Strong([html.Span("Utility function - "), html.Span(id="um_heading")]),
            style=header_style,
            className=header_class,
        ),
        html.Div(
            [
                html.Div(
                    [
                        dcc.Dropdown(
                            id="um_dropdown",
                            options=[
                                {
                                    "label": "Tversky Kahneman utility function",
                                    "value": "TKU",
                                },
                                {"label": "Linear Utility function", "value": "LU",},
                                {"label": "Root utility function", "value": "RU",},
                                {
                                    "label": "Exponential utiltiy function",
                                    "value": "EXU",
                                },
                                {"label": "Bernoulli utility function", "value": "BU",},
                                {"label": "Your utility function", "value": "YU",},
                            ],
                            value="TKU",
                            className="py-2 d-print-none",
                        ),
                        dbc.Collapse(
                            [
                                dbc.Label("Your utility function:"),
                                # MARK Textarea for ASTEVAL
                                dbc.Input(
                                    id="um_text",
                                    type="text",
                                    placeholder="Input your own function",
                                    debounce=True,
                                ),
                                dbc.Button(
                                    "Run Function",
                                    id="um_text_runner",
                                    className="mt-2",
                                ),
                            ],
                            id="um_collapse_YU",
                            className="py-2",
                        ),
                        dbc.Collapse(
                            [
                                dbc.Label("Formula:"),
                                html.Div(fd.um_func_dict["TKU"][2], className="pb-2"),
                                dbc.FormGroup(
                                    [
                                        dbc.Label("a:", width=3, className="my-1",),
                                        dbc.Col(
                                            dbc.Input(
                                                id="um_TKU_a",
                                                type="number",
                                                value=0.88,
                                                step=0.1,
                                            ),
                                            width=9,
                                        ),
                                        dbc.Label("l:", width=3, className="my-1",),
                                        dbc.Col(
                                            dbc.Input(
                                                id="um_TKU_l",
                                                type="number",
                                                value=2.25,
                                                step=0.1,
                                            ),
                                            width=9,
                                        ),
                                        dbc.Label("r:", width=3, className="my-1",),
                                        dbc.Col(
                                            dbc.Input(
                                                id="um_TKU_r",
                                                type="number",
                                                value=0.0,
                                                step=1,
                                            ),
                                            width=9,
                                        ),
                                    ],
                                    row=True,
                                ),
                            ],
                            id="um_collapse_TKU",
                            className="py-2",
                        ),
                        dbc.Collapse(
                            [
                                dbc.Label("Formula:"),
                                html.Div(fd.um_func_dict["RU"][2], className="pb-2"),
                                dbc.FormGroup(
                                    [
                                        dbc.Label("exp:", width=3, className="my-1",),
                                        dbc.Col(
                                            dbc.Input(
                                                id="um_RU_exp",
                                                type="number",
                                                value=2.0,
                                                step=1,
                                            ),
                                            width=9,
                                        ),
                                    ],
                                    row=True,
                                ),
                            ],
                            id="um_collapse_RU",
                            className="py-2",
                        ),
                        dbc.Collapse(
                            [
                                dbc.Label("Formula:"),
                                html.Div(fd.um_func_dict["EXU"][2], className="pb-2"),
                                dbc.FormGroup(
                                    [
                                        dbc.Label("a:", width=3, className="my-1",),
                                        dbc.Col(
                                            dbc.Input(
                                                id="um_EXU_a",
                                                type="number",
                                                value=1.0,
                                                step=0.01,
                                            ),
                                            width=9,
                                        ),
                                    ],
                                    row=True,
                                ),
                            ],
                            id="um_collapse_EXU",
                            className="py-2",
                        ),
                        dbc.Collapse(
                            [
                                dbc.Label("Formula:"),
                                html.Div(fd.um_func_dict["BU"][2], className="pb-2"),
                                dbc.FormGroup(
                                    [
                                        dbc.Label("a:", width=3, className="my-1",),
                                        dbc.Col(
                                            dbc.Input(
                                                id="um_BU_a",
                                                type="number",
                                                value=0.0,
                                                step=0.01,
                                            ),
                                            width=9,
                                        ),
                                    ],
                                    row=True,
                                ),
                            ],
                            id="um_collapse_BU",
                            className="py-2",
                        ),
                        dbc.Collapse(
                            [
                                dbc.Label("Formula:"),
                                html.Div(fd.um_func_dict["LU"][2], className="pb-2"),
                            ],
                            id="um_collapse_LU",
                            className="py-2",
                        ),
                        dbc.Button(
                            "Reset all values",
                            id="um_reset_btn",
                            className="my-3 d-print-none",
                        ),
                    ],
                    className="col",
                ),
                html.Div(
                    [
                        dcc.Graph(id="um_graph"),
                        dbc.FormGroup(
                            [
                                dbc.Label(
                                    "Minimum display value:", width=3, className="my-1",
                                ),
                                dbc.Col(
                                    dbc.Input(
                                        id="um_min_value", type="number", value=0,
                                    ),
                                    width=3,
                                ),
                                dbc.Label(
                                    "Maximum display value:", width=3, className="my-1",
                                ),
                                dbc.Col(
                                    dbc.Input(
                                        id="um_max_value", type="number", value=10,
                                    ),
                                    width=3,
                                ),
                            ],
                            row=True,
                            className="my-2 d-print-none",
                        ),
                    ],
                    className="col-8",
                ),
            ],
            className="row mt-2",
        ),
    ],
)


@app.callback(
    [
        Output("um_TKU_a", "value"),
        Output("um_TKU_l", "value"),
        Output("um_TKU_r", "value"),
        Output("um_RU_exp", "value"),
        Output("um_EXU_a", "value"),
        Output("um_BU_a", "value"),
        Output("um_min_value", "value"),
        Output("um_max_value", "value"),
    ],
    [Input("um_reset_btn", "n_clicks")],
)
def um_reset(n_clicks):
    # Reset all parameters for the utility function
    return (
        0.88,
        2.25,
        0,
        2,
        1,
        0,
        0,
        10,
    )


@app.callback(
    [
        Output("um_collapse_TKU", "is_open"),
        Output("um_collapse_RU", "is_open"),
        Output("um_collapse_LU", "is_open"),
        Output("um_collapse_BU", "is_open"),
        Output("um_collapse_EXU", "is_open"),
        Output("um_collapse_YU", "is_open"),
    ],
    [Input("um_dropdown", "value")],
    [
        State("um_collapse_TKU", "is_open"),
        State("um_collapse_RU", "is_open"),
        State("um_collapse_LU", "is_open"),
        State("um_collapse_BU", "is_open"),
        State("um_collapse_EXU", "is_open"),
        State("um_collapse_YU", "is_open"),
    ],
)
def toggle_um_params(
    drop_val, TKU_open, RU_open, LU_open, BU_open, EXU_open, YU_open,
):
    (TKU_open, RU_open, LU_open, BU_open, EXU_open, YU_open,) = (
        False,
        False,
        False,
        False,
        False,
        False,
    )
    if drop_val == "TKU":
        TKU_open = True
    elif drop_val == "RU":
        RU_open = True
    elif drop_val == "LU":
        LU_open = True
    elif drop_val == "BU":
        BU_open = True
    elif drop_val == "EXU":
        EXU_open = True
    elif drop_val == "YU":
        YU_open = True
    return (
        TKU_open,
        RU_open,
        LU_open,
        BU_open,
        EXU_open,
        YU_open,
    )


@app.callback(
    [
        Output("um_graph", "figure"),
        Output("danger_toast_1", "children"),
        Output("danger_toast_1", "is_open"),
    ],
    [
        Input("um_dropdown", "value"),
        Input("um_min_value", "value"),
        Input("um_max_value", "value"),
        Input("um_TKU_a", "value"),
        Input("um_TKU_l", "value"),
        Input("um_TKU_r", "value"),
        Input("um_RU_exp", "value"),
        Input("um_BU_a", "value"),
        Input("um_EXU_a", "value"),
        Input("um_text_runner", "n_clicks"),
        Input("um_text", "value"),
    ],
)
def update_um_graph(
    um_drop_val,
    min_val,
    max_val,
    TKU_a,
    TKU_l,
    TKU_r,
    RU_exp,
    BU_a,
    EXU_a,
    n_clicks,
    user_func,
):
    if um_drop_val == "TKU":
        kwargs = {"a": TKU_a, "l": TKU_l, "r": TKU_r}
    elif um_drop_val == "RU":
        kwargs = {"exp": RU_exp}
    elif um_drop_val == "LU":
        kwargs = {}
    elif um_drop_val == "BU":
        kwargs = {"a": BU_a}
    elif um_drop_val == "EXU":
        kwargs = {"a": EXU_a}
    elif um_drop_val == "YU":
        kwargs = {"text": user_func}

    x_1_data = np.linspace(min_val, max_val, 100)
    # y_1_data = [fd.um_func_dict[um_drop_val][0](float(i), **kwargs) for i in x_1_data]

    danger_text = ""
    danger_bool = False
    y_1_data = []

    for i in x_1_data:
        try:
            y_1_data.append(fd.um_func_dict[um_drop_val][0](float(i), **kwargs))
        except ce.PositiveValuesOnlyError:
            y_1_data.append(nan)
            danger_text = (
                "The utility function you chose doesn't process negative values"
            )
            danger_bool = True

    fig = go.Figure(
        data=[
            go.Scatter(
                x=x_1_data,
                y=y_1_data,
                line=dict(color=plot_color, width=4,),
                marker=dict(color=plot_color),
            )
        ]
    )
    fig.update_layout(
        template="plotly_white",
        margin=dict(l=25, r=25, b=25, t=25, pad=0),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        # title="Utility function",
        xaxis_title="Payoff",
        yaxis_title="Utility",
        height=300,
    )
    fig.update_xaxes(
        showgrid=False,
        # zeroline=False
    )
    fig.update_yaxes(showgrid=False)

    return fig, danger_text, danger_bool


pw_segment = dbc.Collapse(
    [
        html.H3(
            html.Strong(
                [
                    html.Span("Probability weighting function - "),
                    html.Span(id="pw_heading"),
                ]
            ),
            style=header_style,
            className=header_class,
        ),
        html.Div(
            [
                html.Div(
                    [
                        dcc.Dropdown(
                            id="pw_dropdown",
                            options=[
                                {
                                    "label": "Tversky Kahneman weighting function",
                                    "value": "TKW",
                                },
                                {
                                    "label": "Goldstein Einhorn weigting function",
                                    "value": "GEW",
                                },
                                {"label": "Prelec weighting function", "value": "PW",},
                                {"label": "Linear weighting function", "value": "LW",},
                                {"label": "Power weighting function", "value": "POW",},
                                {"label": "Your weighting function", "value": "YW",},
                            ],
                            value="TKW",
                            className="py-2 d-print-none",
                        ),
                        dbc.Collapse(
                            [
                                dbc.Label("Your probability weighting function:"),
                                # MARK Textarea for ASTEVAL
                                dbc.Input(
                                    id="pw_text",
                                    type="text",
                                    placeholder="Input your own function",
                                    debounce=True,
                                ),
                                dbc.Button(
                                    "Run Function",
                                    id="pw_text_runner",
                                    className="mt-2",
                                ),
                            ],
                            id="pw_collapse_YW",
                            className="py-2",
                        ),
                        dbc.Collapse(
                            [
                                dbc.Label("Formula:"),
                                html.Div(fd.pw_func_dict["TKW"][2], className="pb-2",),
                                dbc.FormGroup(
                                    [
                                        dbc.Label("d:", width=3, className="my-1",),
                                        dbc.Col(
                                            dbc.Input(
                                                id="pw_TKW_d",
                                                type="number",
                                                value=0.65,
                                                min=0,
                                                step=0.01,
                                            ),
                                            width=9,
                                        ),
                                    ],
                                    row=True,
                                ),
                            ],
                            id="pw_collapse_TKW",
                            className="py-2",
                        ),
                        dbc.Collapse(
                            [
                                dbc.Label("Formula:"),
                                html.Div(fd.pw_func_dict["GEW"][2], className="pb-2",),
                                dbc.FormGroup(
                                    [
                                        dbc.Label("b:", width=3, className="my-1",),
                                        dbc.Col(
                                            dbc.Input(
                                                id="pw_GEW_b",
                                                type="number",
                                                value=0.5,
                                                min=0,
                                                max=1,
                                                step=0.01,
                                            ),
                                            width=9,
                                        ),
                                        dbc.Label("a:", width=3, className="my-1",),
                                        dbc.Col(
                                            dbc.Input(
                                                id="pw_GEW_a",
                                                type="number",
                                                value=0.6,
                                                min=0,
                                                max=1,
                                                step=0.01,
                                            ),
                                            width=9,
                                        ),
                                    ],
                                    row=True,
                                ),
                            ],
                            id="pw_collapse_GEW",
                            className="py-2",
                        ),
                        dbc.Collapse(
                            [
                                dbc.Label("Formula:"),
                                html.Div(fd.pw_func_dict["PW"][2], className="pb-2",),
                                dbc.FormGroup(
                                    [
                                        dbc.Label("b:", width=3, className="my-1",),
                                        dbc.Col(
                                            dbc.Input(
                                                id="pw_PW_b",
                                                type="number",
                                                value=0.5,
                                                min=0,
                                                max=1,
                                                step=0.01,
                                            ),
                                            width=9,
                                        ),
                                        dbc.Label("a:", width=3, className="my-1",),
                                        dbc.Col(
                                            dbc.Input(
                                                id="pw_PW_a",
                                                type="number",
                                                value=0.6,
                                                min=0,
                                                max=1,
                                                step=0.01,
                                            ),
                                            width=9,
                                        ),
                                    ],
                                    row=True,
                                ),
                            ],
                            id="pw_collapse_PW",
                            className="py-2",
                        ),
                        dbc.Collapse(
                            [
                                dbc.Label("Formula:"),
                                html.Div(fd.pw_func_dict["LW"][2], className="pb-2",),
                            ],
                            id="pw_collapse_LW",
                            className="py-2",
                        ),
                        dbc.Collapse(
                            [
                                dbc.Label("Formula:"),
                                html.Div(fd.pw_func_dict["POW"][2], className="pb-2",),
                                dbc.FormGroup(
                                    [
                                        dbc.Label("r:", width=3, className="my-1",),
                                        dbc.Col(
                                            dbc.Input(
                                                id="pw_POW_r",
                                                type="number",
                                                value=1,
                                                step=1,
                                            ),
                                            width=9,
                                        ),
                                    ],
                                    row=True,
                                ),
                            ],
                            id="pw_collapse_POW",
                            className="py-2",
                        ),
                        dbc.Button(
                            "Reset all values",
                            id="pw_reset_btn",
                            className="my-3 d-print-none",
                        ),
                    ],
                    className="col",
                ),
                html.Div(
                    [
                        dcc.Graph(id="pw_graph"),
                        dbc.FormGroup(
                            [
                                dbc.Label(
                                    "Minimum display value:", width=3, className="my-1",
                                ),
                                dbc.Col(
                                    dbc.Input(
                                        id="pw_min_value",
                                        type="number",
                                        value=0,
                                        min=0,
                                        max=1,
                                        step=0.01,
                                    ),
                                    width=3,
                                ),
                                dbc.Label(
                                    "Maximum display value:", width=3, className="my-1",
                                ),
                                dbc.Col(
                                    dbc.Input(
                                        id="pw_max_value",
                                        type="number",
                                        value=1,
                                        min=0,
                                        max=1,
                                        step=0.01,
                                    ),
                                    width=3,
                                ),
                            ],
                            row=True,
                            className="my-2 d-print-none",
                        ),
                    ],
                    className="col-8",
                ),
            ],
            className="row mt-2",
        ),
    ],
    id="pw_panel_collapse",
)


@app.callback(
    [
        Output("pw_TKW_d", "value"),
        Output("pw_GEW_b", "value"),
        Output("pw_GEW_a", "value"),
        Output("pw_PW_b", "value"),
        Output("pw_PW_a", "value"),
        Output("pw_POW_r", "value"),
        Output("pw_min_value", "value"),
        Output("pw_max_value", "value"),
    ],
    [Input("pw_reset_btn", "n_clicks")],
)
def pw_reset(n_clicks):
    #  Reset all parameters for the probability weighting function
    return 0.65, 0.5, 0.6, 0.5, 0.6, 2, 0, 1


@app.callback(
    [
        Output("pw_collapse_TKW", "is_open"),
        Output("pw_collapse_GEW", "is_open"),
        Output("pw_collapse_PW", "is_open"),
        Output("pw_collapse_LW", "is_open"),
        Output("pw_collapse_POW", "is_open"),
        Output("pw_collapse_YW", "is_open"),
    ],
    [Input("pw_dropdown", "value")],
    [
        State("pw_collapse_TKW", "is_open"),
        State("pw_collapse_GEW", "is_open"),
        State("pw_collapse_PW", "is_open"),
        State("pw_collapse_LW", "is_open"),
        State("pw_collapse_POW", "is_open"),
        State("pw_collapse_YW", "is_open"),
    ],
)
def toggle_pw_params(drop_val, TKW_open, GEW_open, PW_open, LW_open, POW_open, YW_open):
    TKW_open, GEW_open, PW_open, LW_open, POW_open, YW_open = (
        False,
        False,
        False,
        False,
        False,
        False,
    )
    if drop_val == "TKW":
        TKW_open = True
    elif drop_val == "GEW":
        GEW_open = True
    elif drop_val == "PW":
        PW_open = True
    elif drop_val == "LW":
        LW_open = True
    elif drop_val == "POW":
        POW_open = True
    elif drop_val == "YW":
        YW_open = True
    return TKW_open, GEW_open, PW_open, LW_open, POW_open, YW_open


@app.callback(
    Output("pw_graph", "figure"),
    [
        Input("pw_dropdown", "value"),
        Input("pw_min_value", "value"),
        Input("pw_max_value", "value"),
        Input("pw_TKW_d", "value"),
        Input("pw_GEW_b", "value"),
        Input("pw_GEW_a", "value"),
        Input("pw_PW_b", "value"),
        Input("pw_PW_a", "value"),
        Input("pw_POW_r", "value"),
        Input("pw_text_runner", "n_clicks"),
        Input("pw_text", "value"),
    ],
)
def update_pw_graph(
    pw_drop_val,
    min_val,
    max_val,
    TKW_d,
    GEW_b,
    GEW_a,
    PW_b,
    PW_a,
    POW_r,
    n_clicks,
    user_func,
):
    if pw_drop_val == "TKW":
        kwargs = {"d": TKW_d}
    elif pw_drop_val == "GEW":
        kwargs = {"b": GEW_b, "a": GEW_a}
    elif pw_drop_val == "PW":
        kwargs = {"b": PW_b, "a": PW_a}
    elif pw_drop_val == "LW":
        kwargs = {}
    elif pw_drop_val == "POW":
        kwargs = {"r": POW_r}
    elif pw_drop_val == "YW":
        kwargs = {"text": user_func}

    x_1_data = np.linspace(min_val, max_val, 100)
    y_1_data = [fd.pw_func_dict[pw_drop_val][0](float(i), **kwargs) for i in x_1_data]

    fig = go.Figure(
        data=[
            go.Scatter(
                x=x_1_data,
                y=y_1_data,
                line=dict(color=plot_color, width=4),
                marker=dict(color=plot_color),
            )
        ]
    )
    fig.update_layout(
        template="plotly_white",
        margin=dict(l=25, r=25, b=25, t=25, pad=0),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        # title="Probability weighting function",
        xaxis_title="Probability",
        yaxis_title="Weighted Probability",
        height=300,
        yaxis_tickformat="%",
        xaxis_tickformat="%",
    )
    fig.update_xaxes(
        showgrid=False,
        # zeroline=False
    )
    fig.update_yaxes(showgrid=False)
    return fig


rg_segment = dbc.Collapse(
    [
        html.H3(
            html.Strong([html.Span("Regret function - "), html.Span(id="rg_heading")]),
            id="rg_link",
            style=header_style,
            className=header_class,
        ),
        html.Div(
            [
                html.Div(
                    [
                        dcc.Dropdown(
                            id="rg_dropdown",
                            options=[
                                {"label": "Loomes and Sugden 1982", "value": "LS",},
                                {"label": "Your regret function", "value": "YR",},
                            ],
                            value="LS",
                            className="py-2 d-print-none",
                        ),
                        dbc.Collapse(
                            [
                                dbc.Label("Your Regret function:"),
                                # MARK Textarea for ASTEVAL
                                dbc.Input(
                                    id="rg_text",
                                    type="text",
                                    placeholder="Input your own function",
                                    debounce=True,
                                ),
                                dbc.Button(
                                    "Run Function",
                                    id="rg_text_runner",
                                    className="mt-2",
                                ),
                            ],
                            id="rg_collapse_YR",
                            className="py-2",
                        ),
                        dbc.Collapse(
                            [
                                dbc.Label("Formula:"),
                                html.Div(
                                    fd.rg_func_dict["LS"][
                                        2
                                    ],  # TODO pull this into its own dict and add formula in latex
                                    className="pb-2",
                                ),
                                dbc.FormGroup(
                                    [
                                        dbc.Label(
                                            "weight:", width=3, className="my-1",
                                        ),
                                        dbc.Col(
                                            dbc.Input(
                                                id="rg_LS_weight",
                                                type="number",
                                                value=1,
                                                step=0.01,
                                                min=0,
                                                max=1,
                                            ),
                                            width=9,
                                        ),
                                    ],
                                    row=True,
                                ),
                            ],
                            id="rg_collapse_LS",
                            className="py-2",
                        ),
                        dbc.Button(
                            "Reset all values",
                            id="rg_reset_btn",
                            className="my-3 d-print-none",
                        ),
                    ],
                    className="col",
                ),
                html.Div(
                    [
                        dcc.Graph(id="rg_graph"),
                        dbc.FormGroup(
                            [
                                dbc.Label(
                                    "Minimum display value:", width=3, className="my-1",
                                ),
                                dbc.Col(
                                    dbc.Input(
                                        id="rg_min_value",
                                        type="number",
                                        value=0,
                                        step=1,
                                    ),
                                    width=3,
                                ),
                                dbc.Label(
                                    "Maximum display value:", width=3, className="my-1",
                                ),
                                dbc.Col(
                                    dbc.Input(
                                        id="rg_max_value",
                                        type="number",
                                        value=1,
                                        step=1,
                                    ),
                                    width=3,
                                ),
                            ],
                            row=True,
                            className="my-2 d-print-none",
                        ),
                    ],
                    className="col-8",
                ),
            ],
            className="row mt-2",
        ),
    ],
    id="rg_panel_collapse",
)


@app.callback(
    [
        Output("rg_LS_weight", "value"),
        Output("rg_min_value", "value"),
        Output("rg_max_value", "value"),
    ],
    [Input("rg_reset_btn", "n_clicks")],
)
def rg_reset(n_clicks):
    #  Reset all parameters for the probability weighting function
    return 1, 0, 1


@app.callback(
    [Output("rg_collapse_LS", "is_open"), Output("rg_collapse_YR", "is_open"),],
    [Input("rg_dropdown", "value")],
    [State("rg_collapse_LS", "is_open"), State("rg_collapse_YR", "is_open"),],
)
def toggle_rg_params(drop_val, LS_open, YR_open):
    LS_open, YR_open = False, False
    if drop_val == "LS":
        LS_open = True
    elif drop_val == "YR":
        YR_open = True
    return LS_open, YR_open


@app.callback(
    Output("rg_graph", "figure"),
    [
        Input("rg_dropdown", "value"),
        Input("rg_min_value", "value"),
        Input("rg_max_value", "value"),
        Input("rg_LS_weight", "value"),
        Input("rg_text_runner", "n_clicks"),
        Input("rg_text", "value"),
        # um_info
        Input("um_dropdown", "value"),
        Input("um_TKU_a", "value"),
        Input("um_TKU_l", "value"),
        Input("um_TKU_r", "value"),
        Input("um_RU_exp", "value"),
        Input("um_BU_a", "value"),
        Input("um_EXU_a", "value"),
        Input("um_text_runner", "n_clicks"),
        Input("um_text", "value"),
    ],
)
def update_rg_graph(
    rg_drop_val,
    min_val,
    max_val,
    LS_weight,
    n_clicks,
    rg_user_func,
    # um_ingo
    um_drop_val,
    TKU_a,
    TKU_l,
    TKU_r,
    RU_exp,
    BU_a,
    EXU_a,
    um_n_clicks,
    um_user_func,
):
    # um_info
    if um_drop_val == "TKU":
        um_kwargs = {"a": TKU_a, "l": TKU_l, "r": TKU_r}
    elif um_drop_val == "RU":
        um_kwargs = {"exp": RU_exp}
    elif um_drop_val == "LU":
        um_kwargs = {}
    elif um_drop_val == "BU":
        um_kwargs = {"a": BU_a}
    elif um_drop_val == "EXU":
        um_kwargs = {"a": EXU_a}
    elif um_drop_val == "YU":
        um_kwargs = {"text": um_user_func}

    # rg params
    if rg_drop_val == "LS":
        rg_kwargs = {"weight": LS_weight}
    elif rg_drop_val == "YR":
        rg_kwargs = {
            "text": rg_user_func,
        }

    x_1_data = np.linspace(min_val, max_val, 10)
    y_1_data = np.linspace(min_val, max_val, 10)
    z_1_data = [
        [
            fd.rg_func_dict[rg_drop_val][0](
                x_1_data[i_inner],
                y_1_data[i_outer],
                um_function=fd.um_func_dict[um_drop_val][0],
                um_kwargs=um_kwargs,
                **rg_kwargs
            )
            for i_inner in range(len(x_1_data))
        ]
        for i_outer in range(len(y_1_data))
    ]

    # z_1_data = [[1] * 10] * 10

    fig = go.Figure(
        data=[go.Heatmap(x=x_1_data, y=y_1_data, z=z_1_data, colorscale=heat_scale,)]
    )
    fig.update_layout(
        template="plotly_white",
        margin=dict(l=25, r=25, b=25, t=25, pad=0),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        # title="Utility function",
        xaxis_title="Primary Lottery",
        yaxis_title="Context Lottery",
        height=300,
    )
    # fig.update_xaxes(showgrid=False, zeroline=False)
    # fig.update_yaxes(showgrid=False)
    return fig


sl_segment = dbc.Collapse(
    [
        html.H3(
            html.Strong(
                [html.Span("Salience function - "), html.Span(id="sl_heading")]
            ),
            id="sl_link",
            style=header_style,
            className=header_class,
        ),
        html.Div(
            [
                html.Div(
                    [
                        dcc.Dropdown(
                            id="sl_dropdown",
                            options=[
                                {"label": "Original Salience function", "value": "OG",},
                                {"label": "Your salience function", "value": "YS",},
                            ],
                            value="OG",
                            className="py-2 d-print-none",
                        ),
                        dbc.Collapse(
                            [
                                dbc.Label("Your Salience function:"),
                                # MARK Textarea for ASTEVAL
                                dbc.Input(
                                    id="sl_text",
                                    type="text",
                                    placeholder="Input your own function",
                                    debounce=True,
                                ),
                                dbc.Button(
                                    "Run Function",
                                    id="sl_text_runner",
                                    className="mt-2",
                                ),
                            ],
                            id="sl_collapse_YS",
                            className="py-2",
                        ),
                        dbc.Collapse(
                            [
                                dbc.Label("Formula:"),
                                html.Div(
                                    fd.sl_func_dict["OG"][
                                        2
                                    ],  # TODO pull this into its own dict and add formula in latex
                                    className="pb-2",
                                ),
                                dbc.FormGroup(
                                    [
                                        dbc.Label("theta:", width=3, className="my-1",),
                                        dbc.Col(
                                            dbc.Input(
                                                id="sl_OG_theta",
                                                type="number",
                                                value=0.1,
                                                step=0.01,
                                                min=0,
                                                max=1,
                                            ),
                                            width=9,
                                        ),
                                    ],
                                    row=True,
                                ),
                            ],
                            id="sl_collapse_OG",
                            className="py-2",
                        ),
                        dbc.Button(
                            "Reset all values",
                            id="sl_reset_btn",
                            className="my-3 d-print-none",
                        ),
                    ],
                    className="col",
                ),
                html.Div(
                    [
                        dcc.Graph(id="sl_graph"),
                        dbc.FormGroup(
                            [
                                dbc.Label(
                                    "Minimum display value:", width=3, className="my-1",
                                ),
                                dbc.Col(
                                    dbc.Input(
                                        id="sl_min_value",
                                        type="number",
                                        value=0,
                                        step=1,
                                    ),
                                    width=3,
                                ),
                                dbc.Label(
                                    "Maximum display value:", width=3, className="my-1",
                                ),
                                dbc.Col(
                                    dbc.Input(
                                        id="sl_max_value",
                                        type="number",
                                        value=1,
                                        step=1,
                                    ),
                                    width=3,
                                ),
                            ],
                            row=True,
                            className="my-2 d-print-none",
                        ),
                    ],
                    className="col-8",
                ),
            ],
            className="row mt-2",
        ),
    ],
    id="sl_panel_collapse",
)


@app.callback(
    [
        Output("sl_delta", "value"),
        Output("sl_OG_theta", "value"),
        Output("sl_min_value", "value"),
        Output("sl_max_value", "value"),
    ],
    [Input("sl_reset_btn", "n_clicks")],
)
def rg_reset(n_clicks):
    #  Reset all parameters for the probability weighting function
    return 0.5, 0.1, 0, 1


@app.callback(
    [Output("sl_collapse_OG", "is_open"), Output("sl_collapse_YS", "is_open"),],
    [Input("sl_dropdown", "value")],
    [State("sl_collapse_OG", "is_open"), State("sl_collapse_YS", "is_open"),],
)
def toggle_rg_params(drop_val, OG_open, YS_open):
    OG_open, YS_open = False, False
    if drop_val == "OG":
        OG_open = True
    elif drop_val == "YS":
        YS_open = True
    return OG_open, YS_open


@app.callback(
    Output("sl_graph", "figure"),
    [
        Input("sl_dropdown", "value"),
        Input("sl_min_value", "value"),
        Input("sl_max_value", "value"),
        Input("sl_OG_theta", "value"),
        Input("sl_text_runner", "n_clicks"),
        Input("sl_text", "value"),
    ],
)
def update_sl_graph(
    sl_drop_val, min_val, max_val, OG_theta, n_clicks, user_func,
):
    if sl_drop_val == "OG":
        sl_kwargs = {"theta": OG_theta}
    elif sl_drop_val == "YS":
        sl_kwargs = {"text": user_func}

    x_1_data = np.linspace(min_val, max_val, 10)
    y_1_data = np.linspace(min_val, max_val, 10)
    z_1_data = [
        [
            fd.sl_func_dict[sl_drop_val][0](
                x_1_data[i_inner], y_1_data[i_outer], **sl_kwargs
            )
            for i_inner in range(len(x_1_data))
        ]
        for i_outer in range(len(y_1_data))
    ]

    # z_1_data = [[1] * 10] * 10

    fig = go.Figure(
        data=[go.Heatmap(x=x_1_data, y=y_1_data, z=z_1_data, colorscale=heat_scale,)]
    )
    fig.update_layout(
        template="plotly_white",
        margin=dict(l=25, r=25, b=25, t=25, pad=0),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        # title="Probability weighting function",
        xaxis_title="Primary Lottery",
        yaxis_title="Context Lottery",
        height=300,
    )
    # fig.update_xaxes(showgrid=False, zeroline=False)
    # fig.update_yaxes(showgrid=False)
    return fig


sdt_segment = dbc.Collapse(
    [
        html.H3(
            html.Strong([html.Span("Bivu function - "), html.Span(id="sdt_heading")]),
            id="sdt_link",
            style=header_style,
            className=header_class,
        ),
        html.Div(
            [
                html.Div(
                    [
                        dcc.Dropdown(
                            id="sdt_dropdown",
                            options=[
                                {"label": "Additive Habits function", "value": "AH",},
                                {"label": "Your BIVU function", "value": "YB",},
                            ],
                            value="AH",
                            className="py-2 d-print-none",
                        ),
                        dbc.Collapse(
                            [
                                dbc.Label("Your Bivu function:"),
                                # MARK Textarea for ASTEVAL
                                dbc.Input(
                                    id="sdt_text",
                                    type="text",
                                    placeholder="Input your own function",
                                    debounce=True,
                                ),
                                dbc.Button(
                                    "Run Function",
                                    id="sdt_text_runner",
                                    className="mt-2",
                                ),
                            ],
                            id="sdt_collapse_YB",
                            className="py-2",
                        ),
                        dbc.Collapse(
                            [
                                dbc.Label("Formula:"),
                                html.Div(
                                    fd.sdt_func_dict["AH"][
                                        2
                                    ],  # TODO pull this into its own dict and add formula in latex
                                    className="pb-2",
                                ),
                                dbc.FormGroup(
                                    [
                                        dbc.Label(
                                            "$\\eta$:", width=3, className="my-1",
                                        ),
                                        dbc.Col(
                                            dbc.Input(
                                                id="sdt_AH_eta",
                                                type="number",
                                                value=0.1,
                                                step=0.01,
                                                min=0,
                                                max=1,
                                            ),
                                            width=9,
                                        ),
                                    ],
                                    row=True,
                                ),
                            ],
                            id="sdt_collapse_AH",
                            className="py-2",
                        ),
                        dbc.Button(
                            "Reset all values",
                            id="sdt_reset_btn",
                            className="my-3 d-print-none",
                        ),
                    ],
                    className="col",
                ),
                html.Div(
                    [
                        dcc.Graph(id="sdt_graph"),
                        dbc.FormGroup(
                            [
                                dbc.Label(
                                    "Minimum display value:", width=3, className="my-1",
                                ),
                                dbc.Col(
                                    dbc.Input(
                                        id="sdt_min_value",
                                        type="number",
                                        value=0,
                                        step=1,
                                    ),
                                    width=3,
                                ),
                                dbc.Label(
                                    "Maximum display value:", width=3, className="my-1",
                                ),
                                dbc.Col(
                                    dbc.Input(
                                        id="sdt_max_value",
                                        type="number",
                                        value=1,
                                        step=1,
                                    ),
                                    width=3,
                                ),
                            ],
                            row=True,
                            className="my-2 d-print-none",
                        ),
                    ],
                    className="col-8",
                ),
            ],
            className="row mt-2",
        ),
    ],
    id="sdt_panel_collapse",
)


@app.callback(
    [
        Output("sdt_k", "value"),
        Output("sdt_AH_eta", "value"),
        Output("sdt_min_value", "value"),
        Output("sdt_max_value", "value"),
    ],
    [Input("sdt_reset_btn", "n_clicks")],
)
def sdt_reset(n_clicks):
    #  Reset all parameters for the probability weighting function
    return 0.5, 0.1, 0, 1


@app.callback(
    [Output("sdt_collapse_AH", "is_open"), Output("sdt_collapse_YB", "is_open"),],
    [Input("sdt_dropdown", "value")],
    [State("sdt_collapse_AH", "is_open"), State("sdt_collapse_YB", "is_open"),],
)
def toggle_sdt_params(drop_val, AH_open, YB_open):
    AH_open, YB_open = False, False
    if drop_val == "AH":
        AH_open = True
    elif drop_val == "YB":
        YB_open = True
    return AH_open, YB_open


@app.callback(
    Output("sdt_graph", "figure"),
    [
        Input("sdt_dropdown", "value"),
        Input("sdt_min_value", "value"),
        Input("sdt_max_value", "value"),
        Input("sdt_AH_eta", "value"),
        Input("sdt_text_runner", "n_clicks"),
        Input("sdt_text", "value"),
        # um_info
        Input("um_dropdown", "value"),
        Input("um_TKU_a", "value"),
        Input("um_TKU_l", "value"),
        Input("um_TKU_r", "value"),
        Input("um_RU_exp", "value"),
        Input("um_BU_a", "value"),
        Input("um_EXU_a", "value"),
        Input("um_text_runner", "n_clicks"),
        Input("um_text", "value"),
    ],
)
def update_sdt_graph(
    sdt_drop_val,
    min_val,
    max_val,
    AH_eta,
    n_clicks,
    rg_user_func,
    # um_ingo
    um_drop_val,
    TKU_a,
    TKU_l,
    TKU_r,
    RU_exp,
    BU_a,
    EXU_a,
    um_n_clicks,
    um_user_func,
):
    # um_info
    if um_drop_val == "TKU":
        um_kwargs = {"a": TKU_a, "l": TKU_l, "r": TKU_r}
    elif um_drop_val == "RU":
        um_kwargs = {"exp": RU_exp}
    elif um_drop_val == "LU":
        um_kwargs = {}
    elif um_drop_val == "BU":
        um_kwargs = {"a": BU_a}
    elif um_drop_val == "EXU":
        um_kwargs = {"a": EXU_a}
    elif um_drop_val == "YU":
        um_kwargs = {"text": um_user_func}

    # sdt params
    if sdt_drop_val == "AH":
        sdt_kwargs = {"eta": AH_eta}
    elif sdt_drop_val == "YB":
        sdt_kwargs = {
            "text": rg_user_func,
        }

    x_1_data = np.linspace(min_val, max_val, 10)
    y_1_data = np.linspace(min_val, max_val, 10)
    z_1_data = [
        [
            fd.sdt_func_dict[sdt_drop_val][0](
                x_1_data[i_inner],
                y_1_data[i_outer],
                um_function=fd.um_func_dict[um_drop_val][0],
                um_kwargs=um_kwargs,
                **sdt_kwargs
            )
            for i_inner in range(len(x_1_data))
        ]
        for i_outer in range(len(y_1_data))
    ]

    # z_1_data = [[1] * 10] * 10

    fig = go.Figure(
        data=[go.Heatmap(x=x_1_data, y=y_1_data, z=z_1_data, colorscale=heat_scale,)]
    )
    fig.update_layout(
        template="plotly_white",
        margin=dict(l=25, r=25, b=25, t=25, pad=0),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        # title="Utility function",
        xaxis_title="Primary Lottery",
        yaxis_title="Context Lottery",
        height=300,
    )
    # fig.update_xaxes(showgrid=False, zeroline=False)
    # fig.update_yaxes(showgrid=False)
    return fig


# set dynamic headings
@app.callback(
    [
        Output("um_heading", "children"),
        Output("pw_heading", "children"),
        Output("rg_heading", "children"),
        Output("sl_heading", "children"),
        Output("sdt_heading", "children"),
        Output("gl_heading", "children"),
    ],
    [
        Input("um_dropdown", "value"),
        Input("pw_dropdown", "value"),
        Input("rg_dropdown", "value"),
        Input("sl_dropdown", "value"),
        Input("sdt_dropdown", "value"),
        Input("gl_dropdown", "value"),
    ],
)
def set_headings(
    um_drop_val, pw_drop_val, rg_drop_val, sl_drop_val, sdt_drop_val, gl_drop_val
):
    um_title = fd.um_func_dict[um_drop_val][1]
    pw_title = fd.pw_func_dict[pw_drop_val][1]
    rg_title = fd.rg_func_dict[rg_drop_val][1]
    sl_title = fd.sl_func_dict[sl_drop_val][1]
    sdt_title = fd.sdt_func_dict[sdt_drop_val][1]
    gl_title = fd.um_func_dict[gl_drop_val][1]
    return um_title, pw_title, rg_title, sl_title, sdt_title, gl_title


# Initiate warning banners
toast_1 = dbc.Toast(
    "",
    id="danger_toast_1",
    header="Warning - Something isn't right",
    is_open=False,
    dismissable=True,
    icon="danger",
    # style={"position": "fixed", "top": 66, "right": 10, "width": 350},
)
toast_2 = dbc.Toast(
    "",
    id="danger_toast_2",
    header="Warning - Something isn't right",
    is_open=False,
    dismissable=True,
    icon="danger",
    # style={"position": "fixed", "top": 66, "right": 10, "width": 350},
)
toast_3 = dbc.Toast(
    "",
    id="danger_toast_3",
    header="Warning - Something isn't right",
    is_open=False,
    dismissable=True,
    icon="danger",
    # style={"position": "fixed", "top": 66, "right": 10, "width": 350},
)
toast_4 = dbc.Toast(
    "",
    id="danger_toast_4",
    header="Warning - Something isn't right",
    is_open=False,
    dismissable=True,
    icon="danger",
    # style={"position": "fixed", "top": 66, "right": 10, "width": 350},
)
toast_5 = dbc.Toast(
    "",
    id="danger_toast_5",
    header="Warning - Something isn't right",
    is_open=False,
    dismissable=True,
    icon="danger",
    # style={"position": "fixed", "top": 66, "right": 10, "width": 350},
)

