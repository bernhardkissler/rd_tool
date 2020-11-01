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

plot_color = "#0F4C81"
sub_bg_color = "rgba(255,255,255, 0.75)"

from math import isclose, nan

from app import app

theor_segment = html.Div(
    [
        html.H3("Choose a decision theory", className="py-2",),
        dcc.Dropdown(
            id="theor_dropdown",
            options=[
                {"label": "Cumulative prospect theory", "value": "CPT",},
                {"label": "Rank dependent utility", "value": "RDU",},
                {"label": "Expected utility", "value": "EU",},
                {"label": "Regret theory", "value": "RT"},
            ],
            value="CPT",
        ),
    ],
    className="container p-4 my-2",
    style={"background-color": sub_bg_color},
)

# MARK disable choice of pw for certain theories here
@app.callback(
    Output("pw_panel_collapse", "is_open"), [Input("theor_dropdown", "value")],
)
def collapse_pw(drop_val):
    if drop_val in ["EU", "RT"]:
        return False
    else:
        return True


pw_um_segment = html.Div(
    [
        html.Div(
            [
                html.H3("Utility function", id="uf_link", className="py-2",),
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
                                        {
                                            "label": "Bernoulli utility function",
                                            "value": "BU",
                                        },
                                        {
                                            "label": "Root utility function",
                                            "value": "RU",
                                        },
                                        {
                                            "label": "Linear Utility function",
                                            "value": "LU",
                                        },
                                        {
                                            "label": "Your utility function",
                                            "value": "YU",
                                        },
                                    ],
                                    value="TKU",
                                    className="py-2",
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
                                        html.Div(
                                            fd.um_func_dict["TKU"][2], className="pb-2"
                                        ),
                                        dbc.FormGroup(
                                            [
                                                dbc.Label(
                                                    "a:", width=3, className="my-1",
                                                ),
                                                dbc.Col(
                                                    dbc.Input(
                                                        id="um_TKU_a",
                                                        type="number",
                                                        value=0.88,
                                                        step=0.1,
                                                    ),
                                                    width=9,
                                                ),
                                                dbc.Label(
                                                    "l:", width=3, className="my-1",
                                                ),
                                                dbc.Col(
                                                    dbc.Input(
                                                        id="um_TKU_l",
                                                        type="number",
                                                        value=2.25,
                                                        step=0.1,
                                                    ),
                                                    width=9,
                                                ),
                                                dbc.Label(
                                                    "r:", width=3, className="my-1",
                                                ),
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
                                        html.Div(
                                            fd.um_func_dict["RU"][2], className="pb-2"
                                        ),
                                        dbc.FormGroup(
                                            [
                                                dbc.Label(
                                                    "exp:", width=3, className="my-1",
                                                ),
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
                                        html.Div(
                                            fd.um_func_dict["BU"][2], className="pb-2"
                                        ),
                                    ],
                                    id="um_collapse_BU",
                                    className="py-2",
                                ),
                                dbc.Collapse(
                                    [
                                        dbc.Label("Formula:"),
                                        html.Div(
                                            fd.um_func_dict["LU"][2], className="pb-2"
                                        ),
                                    ],
                                    id="um_collapse_LU",
                                    className="py-2",
                                ),
                                dbc.Button(
                                    "Reset all values",
                                    id="um_reset_btn",
                                    className="my-3",
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
                                            "Minimum display value:",
                                            width=4,
                                            className="my-1",
                                        ),
                                        dbc.Col(
                                            dbc.Input(
                                                id="um_min_value",
                                                type="number",
                                                value=0,
                                            ),
                                            width=2,
                                        ),
                                        dbc.Label(
                                            "Maximum display value:",
                                            width=4,
                                            className="my-1",
                                        ),
                                        dbc.Col(
                                            dbc.Input(
                                                id="um_max_value",
                                                type="number",
                                                value=10,
                                            ),
                                            width=2,
                                        ),
                                    ],
                                    row=True,
                                    className="my-2",
                                ),
                            ],
                            className="col-8",
                        ),
                    ],
                    className="row mt-2",
                ),
            ],
            className="container p-4 my-2",
            style={"background-color": sub_bg_color},
        ),
        html.Div(
            [
                html.H3(
                    "Probability weighting function", id="pw_link", className="py-2",
                ),
                dbc.Collapse(
                    [
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
                                                {
                                                    "label": "Prelec weighting function",
                                                    "value": "PW",
                                                },
                                                {
                                                    "label": "Your weighting function",
                                                    "value": "YW",
                                                },
                                            ],
                                            value="TKW",
                                            className="py-2",
                                        ),
                                        dbc.Collapse(
                                            [
                                                dbc.Label(
                                                    "Your probability weighting function:"
                                                ),
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
                                                html.Div(
                                                    fd.pw_func_dict["TKW"][2],
                                                    className="pb-2",
                                                ),
                                                dbc.FormGroup(
                                                    [
                                                        dbc.Label(
                                                            "d:",
                                                            width=3,
                                                            className="my-1",
                                                        ),
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
                                                html.Div(
                                                    fd.pw_func_dict["GEW"][2],
                                                    className="pb-2",
                                                ),
                                                dbc.FormGroup(
                                                    [
                                                        dbc.Label(
                                                            "b:",
                                                            width=3,
                                                            className="my-1",
                                                        ),
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
                                                        dbc.Label(
                                                            "a:",
                                                            width=3,
                                                            className="my-1",
                                                        ),
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
                                                html.Div(
                                                    fd.pw_func_dict["PW"][2],
                                                    className="pb-2",
                                                ),
                                                dbc.FormGroup(
                                                    [
                                                        dbc.Label(
                                                            "b:",
                                                            width=3,
                                                            className="my-1",
                                                        ),
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
                                                        dbc.Label(
                                                            "a:",
                                                            width=3,
                                                            className="my-1",
                                                        ),
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
                                        dbc.Button(
                                            "Reset all values",
                                            id="pw_reset_btn",
                                            className="my-3",
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
                                                    "Minimum display value:",
                                                    width=4,
                                                    className="my-1",
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
                                                    width=2,
                                                ),
                                                dbc.Label(
                                                    "Maximum display value:",
                                                    width=4,
                                                    className="my-1",
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
                                                    width=2,
                                                ),
                                            ],
                                            row=True,
                                            className="my-2",
                                        ),
                                    ],
                                    className="col-8",
                                ),
                            ],
                            className="row mt-2",
                        ),
                    ],
                    id="pw_panel_collapse",
                ),
            ],
            className="container p-4 my-2",
            style={"background-color": sub_bg_color},
        ),
    ],
)


@app.callback(
    [
        Output("pw_TKW_d", "value"),
        Output("pw_GEW_b", "value"),
        Output("pw_GEW_a", "value"),
        Output("pw_PW_b", "value"),
        Output("pw_PW_a", "value"),
        Output("pw_min_value", "value"),
        Output("pw_max_value", "value"),
    ],
    [Input("pw_reset_btn", "n_clicks")],
)
def pw_reset(n_clicks):
    #  Reset all parameters for the probability weighting function
    return 0.65, 0.5, 0.6, 0.5, 0.6, 0, 1


@app.callback(
    [
        Output("um_TKU_a", "value"),
        Output("um_TKU_l", "value"),
        Output("um_TKU_r", "value"),
        Output("um_RU_exp", "value"),
        Output("um_min_value", "value"),
        Output("um_max_value", "value"),
    ],
    [Input("um_reset_btn", "n_clicks")],
)
def um_reset(n_clicks):
    # Reset all parameters for the utility function
    return 0.88, 2.25, 0, 2, 0, 10


@app.callback(
    [
        Output("pw_collapse_TKW", "is_open"),
        Output("pw_collapse_GEW", "is_open"),
        Output("pw_collapse_PW", "is_open"),
        Output("pw_collapse_YW", "is_open"),
    ],
    [Input("pw_dropdown", "value")],
    [
        State("pw_collapse_TKW", "is_open"),
        State("pw_collapse_GEW", "is_open"),
        State("pw_collapse_PW", "is_open"),
        State("pw_collapse_YW", "is_open"),
    ],
)
def toggle_pw_params(drop_val, TKW_open, GEW_open, PW_open, YW_open):
    TKW_open, GEW_open, PW_open, YW_open = False, False, False, False
    if drop_val == "TKW":
        TKW_open = True
    elif drop_val == "GEW":
        GEW_open = True
    elif drop_val == "PW":
        PW_open = True
    elif drop_val == "YW":
        YW_open = True
    return TKW_open, GEW_open, PW_open, YW_open


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
        Input("pw_text_runner", "n_clicks"),
        Input("pw_text", "value"),
    ],
)
def update_pw_graph(
    pw_drop_val, min_val, max_val, TKW_d, GEW_b, GEW_a, PW_b, PW_a, n_clicks, user_func
):
    if pw_drop_val == "TKW":
        kwargs = {"d": TKW_d}
    elif pw_drop_val == "GEW":
        kwargs = {"b": GEW_b, "a": GEW_a}
    elif pw_drop_val == "PW":
        kwargs = {"b": PW_b, "a": PW_a}
    elif pw_drop_val == "YW":
        kwargs = {"text": user_func}

    x_1_data = np.linspace(min_val, max_val, 1000)
    y_1_data = [fd.pw_func_dict[pw_drop_val][0](float(i), **kwargs) for i in x_1_data]

    fig = go.Figure(
        data=[
            go.Scatter(
                x=x_1_data,
                y=y_1_data,
                line=dict(color=plot_color),
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
    )
    fig.update_xaxes(showgrid=False, zeroline=False)
    fig.update_yaxes(showgrid=False)
    return fig


@app.callback(
    [
        Output("um_collapse_TKU", "is_open"),
        Output("um_collapse_RU", "is_open"),
        Output("um_collapse_LU", "is_open"),
        Output("um_collapse_BU", "is_open"),
        Output("um_collapse_YU", "is_open"),
    ],
    [Input("um_dropdown", "value")],
    [
        State("um_collapse_TKU", "is_open"),
        State("um_collapse_RU", "is_open"),
        State("um_collapse_LU", "is_open"),
        State("um_collapse_BU", "is_open"),
        State("um_collapse_YU", "is_open"),
    ],
)
def toggle_um_params(drop_val, TKU_open, RU_open, LU_open, BU_open, YU_open):
    TKU_open, RU_open, LU_open, BU_open, YU_open = False, False, False, False, False
    if drop_val == "TKU":
        TKU_open = True
    elif drop_val == "RU":
        RU_open = True
    elif drop_val == "LU":
        LU_open = True
    elif drop_val == "BU":
        BU_open = True
    elif drop_val == "YU":
        YU_open = True
    return TKU_open, RU_open, LU_open, BU_open, YU_open


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
        Input("um_text_runner", "n_clicks"),
        Input("um_text", "value"),
    ],
)
def update_um_graph(
    um_drop_val, min_val, max_val, TKU_a, TKU_l, TKU_r, RU_exp, n_clicks, user_func
):
    if um_drop_val == "TKU":
        kwargs = {"a": TKU_a, "l": TKU_l, "r": TKU_r}
    elif um_drop_val == "RU":
        kwargs = {"exp": RU_exp}
    elif um_drop_val == "LU":
        kwargs = {}
    elif um_drop_val == "BU":
        kwargs = {}
    elif um_drop_val == "YU":
        kwargs = {"text": user_func}

    x_1_data = np.linspace(min_val, max_val, 1000)
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
                "The utility function you chose does only process positive values"
            )
            danger_bool = True

    fig = go.Figure(
        data=[
            go.Scatter(
                x=x_1_data,
                y=y_1_data,
                line=dict(color=plot_color),
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
    fig.update_xaxes(showgrid=False, zeroline=False)
    fig.update_yaxes(showgrid=False)

    return fig, danger_text, danger_bool


toast_1 = dbc.Toast(
    "",
    id="danger_toast_1",
    header="Warning - Something isn't right",
    is_open=False,
    dismissable=True,
    icon="danger",
    style={"position": "fixed", "top": 66, "right": 10, "width": 350},
)
toast_2 = dbc.Toast(
    "",
    id="danger_toast_2",
    header="Warning - Something isn't right",
    is_open=False,
    dismissable=True,
    icon="danger",
    style={"position": "fixed", "top": 66, "right": 10, "width": 350},
)
toast_3 = dbc.Toast(
    "",
    id="danger_toast_3",
    header="Warning - Something isn't right",
    is_open=False,
    dismissable=True,
    icon="danger",
    style={"position": "fixed", "top": 66, "right": 10, "width": 350},
)

