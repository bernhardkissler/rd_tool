import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import dash_table

import plotly.graph_objs as go

import numpy as np

import rd_functions.main_functions as mf
import rd_functions.util_mod as um
import rd_functions.prob_weighting as pw

import apps.func_dicts as fd

from math import isclose

from app import app

output_segment = dbc.Container(
    [
        html.Hr(),
        html.H3("Output", className="py-2"),
        dbc.CardGroup(
            [
                dbc.Card(
                    dbc.CardBody(
                        [html.H6("Inputs"), dbc.Container(id="output_input_params"),]
                    ),
                ),
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.H6("Decision theory"),
                            dbc.Container(id="output_theor_params"),
                        ]
                    ),
                ),
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.H6("Utility function"),
                            dbc.Container(id="output_um_params"),
                        ]
                    ),
                ),
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.H6("Probability weighting function"),
                            dbc.Container(id="output_pw_params"),
                        ]
                    ),
                ),
                dbc.Card(
                    dbc.CardBody(
                        [html.H6("Result"), dbc.Container(id="output_results_params"),]
                    ),
                ),
            ],
        ),
    ],
    className="px-2",
)


@app.callback(
    Output("output_input_params", "children"),
    [Input("std_input_tbl", "data"), Input("data_entry_tab", "value"),],
)
def update_output_input(
    rows, tab_val_entry,
):
    # if tab_val_entry == "STD":
    probs = [float(i["std_probabilities_tbl"]) for i in rows]
    pays = [float(i["std_payoffs_tbl"]) for i in rows]
    # elif tab_val_entry == "RT":

    return (
        html.P("Payoffs: {}".format(pays)),
        html.P("Probabilities: {}".format(probs)),
    )


@app.callback(
    Output("output_theor_params", "children"), [Input("theor_dropdown", "value"),],
)
def update_output_theor(theor_drop_val):
    return fd.mf_func_dict[theor_drop_val][1]


@app.callback(
    Output("output_um_params", "children"),
    [
        Input("um_dropdown", "value"),
        Input("um_TKU_a", "value"),
        Input("um_TKU_l", "value"),
        Input("um_TKU_r", "value"),
        Input("um_RU_exp", "value"),
    ],
)
def update_output_um_theor(
    um_drop_val, TKU_a, TKU_l, TKU_r, RU_exp,
):
    if um_drop_val == "TKU":
        um_kwargs = {"a": TKU_a, "l": TKU_l, "r": TKU_r}
    elif um_drop_val == "RU":
        um_kwargs = {"exp": RU_exp}
    elif um_drop_val == "LU":
        um_kwargs = {}
    elif um_drop_val == "BU":
        um_kwargs = {}
    elif um_drop_val == "YU":
        um_kwargs = {}
    return (
        html.P("Theory: {}".format(fd.um_func_dict[um_drop_val][1])),
        html.P("Formula: {}".format(fd.um_func_dict[um_drop_val][2])),
        html.P("Parameters: {}".format(um_kwargs)),
    )


@app.callback(
    Output("output_pw_params", "children"),
    [
        Input("pw_dropdown", "value"),
        Input("pw_TKW_d", "value"),
        Input("pw_GEW_b", "value"),
        Input("pw_GEW_a", "value"),
        Input("pw_PW_b", "value"),
        Input("pw_PW_a", "value"),
        Input("theor_dropdown", "value"),
    ],
)
def update_output_pw_theor(
    pw_drop_val, TKW_d, GEW_b, GEW_a, PW_b, PW_a, theor_drop_val
):
    if pw_drop_val == "TKW":
        pw_kwargs = {"d": TKW_d}
    elif pw_drop_val == "GEW":
        pw_kwargs = {"b": GEW_b, "a": GEW_a}
    elif pw_drop_val == "PW":
        pw_kwargs = {"b": PW_b, "a": PW_a}
    elif pw_drop_val == "YW":
        pw_kwargs = {}

    if theor_drop_val == "EU":
        return html.P("EU doesn't allow for pw")
    else:
        return (
            html.P("Theory: {}".format(fd.pw_func_dict[pw_drop_val][1])),
            html.P("Formula: {}".format(fd.pw_func_dict[pw_drop_val][2])),
            html.P("Parameters: {}".format(pw_kwargs)),
        )


@app.callback(
    Output("output_results_params", "children"),
    [
        Input("std_input_tbl", "data"),
        Input("data_entry_tab", "value"),
        Input("theor_dropdown", "value"),
        # pw params
        Input("pw_dropdown", "value"),
        Input("pw_TKW_d", "value"),
        Input("pw_GEW_b", "value"),
        Input("pw_GEW_a", "value"),
        Input("pw_PW_b", "value"),
        Input("pw_PW_a", "value"),
        Input("pw_text_runner", "n_clicks"),
        Input("pw_text", "value"),
        # um params
        Input("um_dropdown", "value"),
        Input("um_TKU_a", "value"),
        Input("um_TKU_l", "value"),
        Input("um_TKU_r", "value"),
        Input("um_RU_exp", "value"),
        Input("um_text_runner", "n_clicks"),
        Input("um_text", "value"),
    ],
)
def update_output(
    rows,
    tab_val_entry,
    theor_drop_val,
    # pw params
    pw_drop_val,
    TKW_d,
    GEW_b,
    GEW_a,
    PW_b,
    PW_a,
    pw_n_clicks,
    pw_user_func,
    # um params
    um_drop_val,
    TKU_a,
    TKU_l,
    TKU_r,
    RU_exp,
    um_n_clicks,
    um_user_func,
):
    # if tab_val_entry == "STD":
    probs = [float(i["std_probabilities_tbl"]) for i in rows]
    pays = [float(i["std_payoffs_tbl"]) for i in rows]
    # elif tab_val_entry == "RT":
    # pw params
    if pw_drop_val == "TKW":
        pw_kwargs = {"d": TKW_d}
    elif pw_drop_val == "GEW":
        pw_kwargs = {"b": GEW_b, "a": GEW_a}
    elif pw_drop_val == "PW":
        pw_kwargs = {"b": PW_b, "a": PW_a}
    elif pw_drop_val == "YW":
        pw_kwargs = {"text": pw_user_func}

    # um params
    if um_drop_val == "TKU":
        um_kwargs = {"a": TKU_a, "l": TKU_l, "r": TKU_r}
    elif um_drop_val == "RU":
        um_kwargs = {"exp": RU_exp}
    elif um_drop_val == "LU":
        um_kwargs = {}
    elif um_drop_val == "BU":
        um_kwargs = {}
    elif um_drop_val == "YU":
        um_kwargs = {"text": um_user_func}

    if theor_drop_val == "EU":
        res = fd.mf_func_dict[theor_drop_val][0](
            pays,
            probs,
            um_function=fd.um_func_dict[um_drop_val][0],
            um_kwargs=um_kwargs,
        )
    else:
        res = fd.mf_func_dict[theor_drop_val][0](
            pays,
            probs,
            um_function=fd.um_func_dict[um_drop_val][0],
            pw_function=fd.pw_func_dict[pw_drop_val][0],
            um_kwargs=um_kwargs,
            pw_kwargs=pw_kwargs,
        )
    return html.P("{}".format(round(res, 4)))
