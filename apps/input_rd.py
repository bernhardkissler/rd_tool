# import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import dash_table

import plotly.graph_objs as go
import plotly.express as px
from plotly.subplots import make_subplots

plot_color = "#F26B5B"

import numpy as np

# import rd_functions.main_functions as mf
# import rd_functions.util_mod as um
# import rd_functions.prob_weighting as pw

# import apps.func_dicts as fd

from math import isclose

from app import app

input_segment = dbc.Container(
    [
        html.Hr(),
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
                                                    id="std_input_tbl",
                                                    columns=(
                                                        [
                                                            {
                                                                "id": "std_probabilities_tbl",
                                                                "name": "Probabilities",
                                                                "type": "numeric",
                                                            }
                                                        ]
                                                        + [
                                                            {
                                                                "id": "std_payoffs_tbl",
                                                                "name": "Payoffs",
                                                                "type": "numeric",
                                                            }
                                                        ]
                                                        + [
                                                            {
                                                                "id": "comp_payoffs_tbl",
                                                                "name": "Comp Payoffs",
                                                                "type": "numeric",
                                                            }
                                                        ]
                                                    ),
                                                    hidden_columns=["comp_payoffs_tbl"],
                                                    style_cell_conditional=[
                                                        {
                                                            "if": {
                                                                "column_id": "std_probabilities_tbl"
                                                            },
                                                            "width": "33%",
                                                        },
                                                        {
                                                            "if": {
                                                                "column_id": "std_payoffs_tbl"
                                                            },
                                                            "width": "33%",
                                                        },
                                                        {
                                                            "if": {
                                                                "column_id": "comp_payoffs_tbl"
                                                            },
                                                            "width": "33%",
                                                        },
                                                    ],
                                                    data=[
                                                        dict(
                                                            std_probabilities_tbl=0.1,
                                                            std_payoffs_tbl=1,
                                                            comp_payoffs_tbl=1,
                                                        ),
                                                        dict(
                                                            std_probabilities_tbl=0.4,
                                                            std_payoffs_tbl=2,
                                                            comp_payoffs_tbl=2,
                                                        ),
                                                        dict(
                                                            std_probabilities_tbl=0.5,
                                                            std_payoffs_tbl=3,
                                                            comp_payoffs_tbl=3,
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
                                            id="std_editing_rows_button",
                                            n_clicks=0,
                                        ),
                                    ],
                                    value="STD",
                                    label="Standard data entry",
                                    id="std_input_tab",
                                ),
                                dcc.Tab(
                                    [
                                        html.Div(
                                            [
                                                dash_table.DataTable(
                                                    id="rt_input_tbl",
                                                    columns=(
                                                        [
                                                            {
                                                                "id": "rt_probabilities_tbl",
                                                                "name": "Probabilities",
                                                                "type": "numeric",
                                                            }
                                                        ]
                                                        + [
                                                            {
                                                                "id": "rt_payoffs_tbl_0",
                                                                "name": "Payoffs",
                                                                "type": "numeric",
                                                            }
                                                        ]
                                                        + [
                                                            {
                                                                "id": "rt_payoffs_tbl_1",
                                                                "name": "Payoffs",
                                                                "type": "numeric",
                                                            }
                                                        ]
                                                    ),
                                                    data=[
                                                        dict(
                                                            rt_probabilities_tbl=0.1,
                                                            rt_payoffs_tbl_0=1,
                                                            rt_payoffs_tbl_1=4,
                                                        ),
                                                        dict(
                                                            rt_probabilities_tbl=0.4,
                                                            rt_payoffs_tbl_0=2,
                                                            rt_payoffs_tbl_1=5,
                                                        ),
                                                        dict(
                                                            rt_probabilities_tbl=0.5,
                                                            rt_payoffs_tbl_0=3,
                                                            rt_payoffs_tbl_1=6,
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
                                            id="rt_editing_rows_button",
                                            n_clicks=0,
                                        ),
                                        dbc.Button(
                                            "Add Column",
                                            id="rt_editing_columns_button",
                                            n_clicks=0,
                                        ),
                                    ],
                                    value="RT",
                                    label="Regret theory entry",
                                    id="rt_input_tab",
                                ),
                            ],
                            id="data_entry_tab",
                            value="STD",
                        ),
                    ],
                    className="col-4",
                ),
                html.Div([dcc.Graph(id="gamble_figs")], className="col",),
            ],
            className="row mt-2",
        ),
        html.Hr(),
    ],
    className="px-2",
)


@app.callback(
    [
        Output("std_input_tab", "disabled"),
        Output("rt_input_tab", "disabled"),
        Output("data_entry_tab", "value"),
    ],
    [Input("theor_dropdown", "value")],
    [State("data_entry_tab", "value")],
)
def manage_input_tabs(drop_val, tab_state):
    if drop_val == "RT":
        return True, False, "RT"
    else:
        return False, True, "STD"


# Manage gamble Figs
@app.callback(
    Output("gamble_figs", "figure"),
    [
        Input("std_input_tbl", "data"),
        Input("rt_input_tbl", "data"),
        Input("rt_input_tbl", "columns"),
        Input("data_entry_tab", "value"),
    ],
)
def update_gamble_figs(std_rows, rt_rows, rt_columns, tab_val_entry):
    probs = list(reversed([float(i["std_probabilities_tbl"]) for i in std_rows]))
    pays = list(reversed([float(i["std_payoffs_tbl"]) for i in std_rows]))
    if tab_val_entry == "RT":
        pays = [
            list(reversed([float(rt_row[rt_column["id"]]) for rt_row in rt_rows]))
            for rt_column in rt_columns
            if rt_column["id"] != "rt_probabilities_tbl"
        ][0]
        probs = list(
            reversed([float(rt_row["rt_probabilities_tbl"]) for rt_row in rt_rows])
        )
    fig = gamble_figs(pays, probs)
    return fig


def gamble_figs(pays, probs):
    # Prepare plot
    fig = make_subplots(
        rows=2,
        cols=2,
        specs=[[{"rowspan": 2}, {}], [None, {}]],
        shared_xaxes=True,
        subplot_titles=(
            "Your Choices",
            "Probability Density Function",
            "Cumulative Density Function",
        ),
    )
    fig.update_layout(
        # title="Cumulative Density Function",
        template="plotly_white",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        # font=dict(color="white"),
        margin=dict(l=0, r=0, t=20, b=0, pad=0,),
        showlegend=False,
        xaxis2_showticklabels=True,
        xaxis3_showticklabels=True,
        height=300,
    )

    # Decision Tree Figure
    y_1 = [0.5] + list(np.linspace(0, 1, len(probs)))
    y_2 = [0.25 + 0.5 * i for i in list(np.linspace(0, 1, len(probs)))]

    for i in range(len(probs)):
        fig.add_trace(
            go.Scatter(
                x=[0, 1],
                y=[0.5, y_1[i + 1]],
                mode="lines",
                line=dict(color=plot_color),
                marker=dict(color=plot_color),
                hoverinfo="none",
            ),
            row=1,
            col=1,
        )
    for i in range(len(probs)):
        fig.add_annotation(
            x=0.5,
            y=y_2[i],
            text=probs[i],
            ax=0,
            ay=-15,
            arrowcolor="rgba(0,0,0,0)",
            row=1,
            col=1,
        )

    for i in range(len(probs)):
        fig.add_annotation(
            x=1,
            y=y_1[i + 1],
            text=pays[i],
            ax=20,
            ay=0,
            arrowcolor="rgba(0,0,0,0)",
            row=1,
            col=1,
        )
    fig.update_xaxes(
        range=[-0.4, 1.4], showgrid=False, zeroline=False, visible=False, row=1, col=1
    )
    fig.update_yaxes(
        range=[-0.1, 1.1], showgrid=False, zeroline=False, visible=False, row=1, col=1
    )

    # PDF Figure Trace
    fig.add_trace(go.Bar(x=pays, y=probs, marker_color=plot_color), row=1, col=2)
    fig.update_xaxes(
        showgrid=False,
        zeroline=False,
        visible=True,
        tickmode="array",
        tickvals=pays,
        row=1,
        col=2,
    )
    fig.update_yaxes(
        showgrid=False, zeroline=True, row=1, col=2,
    )

    # Transformation for cdf
    pays_ord, probs_ord = sorted(pays), [x for _, x in sorted(zip(pays, probs))]
    pays_graph = [
        [pays_ord[i], pays_ord[i + 1]]
        if i < len(pays_ord) - 1
        else [pays_ord[i], pays_ord[i] * 1.1]
        for i in range(len(pays_ord))
    ]
    probs_graph = [
        2 * [sum(probs_ord[: i + 1])] if i < len(probs_ord) else 2 * []
        for i in range(len(probs_ord))
    ]
    for i, _ in enumerate(pays_graph):
        fig.add_trace(
            go.Scatter(
                x=pays_graph[i],
                y=probs_graph[i],
                mode="lines",
                line=dict(color=plot_color),
            ),
            row=2,
            col=2,
        )
    # print(f"pays = {pays_graph}", "\n", f"probs = {probs_graph}")

    fig.update_xaxes(
        showgrid=False,
        zeroline=False,
        visible=True,
        tickmode="array",
        tickvals=pays,
        row=2,
        col=2,
    )
    fig.update_yaxes(
        range=[0.0, 1.05], showgrid=False, zeroline=True, row=2, col=2,
    )
    return fig


# Callbacks for Table
@app.callback(
    [Output("danger_toast_2", "is_open"), Output("danger_toast_2", "children")],
    [Input("std_input_tbl", "data"), Input("data_entry_tab", "value"),],
)
def check_probs(rows, tab_val_entry):
    # TODO check out how best to handle floating point errors
    # if tab_val_entry == "STD":
    probs = [float(i["std_probabilities_tbl"]) for i in rows]
    # elif tab_val_entry == "RT":
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
    Output("std_input_tbl", "data"),
    [Input("std_editing_rows_button", "n_clicks")],
    [State("std_input_tbl", "data"), State("std_input_tbl", "columns")],
)
def add_row(n_clicks, rows, columns):
    if n_clicks > 0:
        rows.append({c["id"]: "" for c in columns})
    return rows


@app.callback(
    Output("rt_input_tbl", "data"),
    [Input("rt_editing_rows_button", "n_clicks")],
    [State("rt_input_tbl", "data"), State("rt_input_tbl", "columns")],
)
def add_row(n_clicks, rows, columns):
    if n_clicks > 0:
        rows.append({c["id"]: "" for c in columns})
    return rows


@app.callback(
    Output("rt_input_tbl", "columns"),
    [Input("rt_editing_columns_button", "n_clicks")],
    [State("rt_input_tbl", "columns")],
)
def update_columns(n_clicks, existing_columns):
    if n_clicks > 0:
        existing_columns.append(
            {
                "id": "rt_payoffs_tbl_{}".format(str(n_clicks + 1)),
                "name": "Payoffs",
                # "renamable": True,
                "deletable": True,
                "type": "numeric",
            }
        )
    return existing_columns
