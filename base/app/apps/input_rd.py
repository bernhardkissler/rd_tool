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

input_segment = dbc.Container(
    [
        # TODO sync the two ways of entering data and maybe split them into different tabs
        html.H3("Enter a gamble", className="py-2"),
        html.Div(
            [
                html.Div(
                    [
                        dcc.Tabs(
                            [
                                dcc.Tab(
                                    [
                                        html.Div(
                                            [
                                                dash_table.DataTable(
                                                    id="input_tbl",
                                                    columns=(
                                                        [
                                                            {
                                                                "id": "payoffs_tbl",
                                                                "name": "Payoffs",
                                                                "type": "numeric",
                                                            }
                                                        ]
                                                        + [
                                                            {
                                                                "id": "probabilities_tbl",
                                                                "name": "Probabilities",
                                                                "type": "numeric",
                                                            }
                                                        ]
                                                    ),
                                                    data=[
                                                        dict(
                                                            payoffs_tbl=1,
                                                            probabilities_tbl=0.1,
                                                        ),
                                                        dict(
                                                            payoffs_tbl=2,
                                                            probabilities_tbl=0.4,
                                                        ),
                                                        dict(
                                                            payoffs_tbl=3,
                                                            probabilities_tbl=0.5,
                                                        ),
                                                    ],
                                                    editable=True,
                                                    row_deletable=True,
                                                ),
                                            ],
                                            className="mx-3 py-2",
                                        ),
                                        dbc.Button(
                                            "Add Row",
                                            id="editing-rows-button",
                                            n_clicks=0,
                                        ),
                                    ],
                                    value="STD",
                                    label="Standard data entry",
                                ),
                                dcc.Tab(
                                    [
                                        html.Div(
                                            [
                                                dbc.Label("Payoffs"),
                                                dbc.Input(
                                                    id="pays_input",
                                                    type="text",
                                                    placeholder="list of payoffs",
                                                    debounce=True,
                                                ),
                                                dbc.Label("Probabilities"),
                                                dbc.Input(
                                                    id="probs_input",
                                                    type="text",
                                                    placeholder="list of probabilities",
                                                    debounce=True,
                                                ),
                                            ],
                                            className="py-2",
                                        )
                                    ],
                                    value="BLK",
                                    label="Bulk data entry",
                                ),
                            ],
                            id="data_entry_tab",
                            value="STD",
                        ),
                    ],
                    className="col-6",
                ),
                html.Div([dcc.Graph(id="gamble_fig"),], className="col"),
            ],
            className="row mt-2",
        ),
        dbc.Alert(id="probs_alert", color="warning", is_open=False, dismissable=True,),
        html.Hr(),
    ],
    className="px-2",
)


@app.callback(
    Output("gamble_fig", "figure"),
    [
        Input("input_tbl", "data"),
        Input("pays_input", "value"),
        Input("probs_input", "value"),
        Input("data_entry_tab", "value"),
    ],
)
def update_gamble_fig(rows, pays_input, probs_input, tab_val_entry):
    if tab_val_entry == "STD":
        probs = list(reversed([float(i["probabilities_tbl"]) for i in rows]))
        pays = list(reversed([float(i["payoffs_tbl"]) for i in rows]))
    elif tab_val_entry == "BLK":
        probs = list(reversed([float(i) for i in probs_input.split(",")]))
        pays = list(reversed([float(i) for i in pays_input.split(",")]))

    fig = gamble_fig(pays, probs)
    return fig


def gamble_fig(pays, probs):
    y_1 = [0.5] + list(np.linspace(0, 1, len(probs)))
    x_1 = [0] + [1] * len(y_1)
    y_2 = [0.25 + 0.5 * i for i in list(np.linspace(0, 1, len(probs)))]

    fig = go.Figure(data=[go.Scatter(x=[], y=[],)])
    for i in range(len(probs)):
        fig.add_annotation(
            x=0.5, y=y_2[i], text=probs[i], ax=0, ay=-15, arrowcolor="white",
        )

    for i in range(len(probs)):
        fig.add_annotation(
            x=1, y=y_1[i + 1], text=pays[i], ax=20, ay=0, arrowcolor="white",
        )
    for i in range(len(probs)):
        fig.add_trace(
            go.Scatter(
                x=[0, 1],
                y=[0.5, y_1[i + 1]],
                mode="markers+lines",
                line=dict(color="#636EFA"),
                marker=dict(color="#636EFA"),
                hoverinfo="none",
            )
        )

    fig.update_layout(
        template="plotly_white",
        margin=dict(l=0, r=0, b=0, t=0, pad=0),
        font=dict(size=18),
        showlegend=False,
    )
    fig.update_xaxes(range=[-0.4, 1.4], showgrid=False, zeroline=False, visible=False)
    fig.update_yaxes(range=[-0.1, 1.1], showgrid=False, zeroline=False, visible=False)

    return fig


@app.callback(
    [Output("probs_alert", "is_open"), Output("probs_alert", "children")],
    [
        Input("input_tbl", "data"),
        Input("probs_input", "value"),
        Input("data_entry_tab", "value"),
    ],
)
def check_probs(rows, probs_input, tab_val_entry):
    # TODO check out how best to handle floating point errors
    if tab_val_entry == "STD":
        probs = [float(i["probabilities_tbl"]) for i in rows]
    elif tab_val_entry == "BLK":
        probs = [float(i) for i in probs_input.split(",")]
        print(probs)
    if not isclose(sum(probs), 1):
        return (
            True,
            "Please make sure that the probabilities of the different payoffs add to 1. In the moment their sum is {}.".format(
                sum(probs)
            ),
        )
    else:
        return False, ""


@app.callback(
    Output("input_tbl", "data"),
    [Input("editing-rows-button", "n_clicks")],
    [State("input_tbl", "data"), State("input_tbl", "columns")],
)
def add_row(n_clicks, rows, columns):
    if n_clicks > 0:
        rows.append({c["id"]: "" for c in columns})
    return rows


@app.callback(
    [Output("pays_input", "value"), Output("probs_input", "value")],
    [Input("input_tbl", "data"), Input("input_tbl", "columns")],
)
def sync_inputs_tbl(rows, columns):
    pays = str([i["payoffs_tbl"] for i in rows])[1:-1]
    probs = str([i["probabilities_tbl"] for i in rows])[1:-1]
    return pays, probs


# TODO Check wether dash has introduced two way syncing at https://community.plotly.com/t/synchronize-components-bidirectionally/14158
# @app.callback(
#     Output("input_tbl", "data"),
#     [Input("pays_input", "value"), Input("probs_input", "value")],
# )
# def sync_inputs_plain(pays, probs):
#     pays_ls = [float(i) for i in pays.split(",")]
#     probs_ls = [float(i) for i in probs.split(",")]
