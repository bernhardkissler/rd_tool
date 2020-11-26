# import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import dash_table
import dash_table.FormatTemplate as FormatTemplate

import plotly.graph_objs as go
import plotly.express as px
from plotly.subplots import make_subplots
import dash_daq as daq

import apps.func_dicts as fd

plot_color = fd.plot_color
prim_color = fd.prim_color

header_style = {"background-color": prim_color}
header_class = "my-2 p-2 text-white rounded"

import numpy as np

# import rd_functions.main_functions as mf
# import rd_functions.util_mod as um
# import rd_functions.prob_weighting as pw
import rd_functions.summary_statistics as sm
import apps.func_dicts as fd


# import apps.func_dicts as fd

from math import isclose

from app import app

stat_table = dbc.Table(
    [
        html.Thead(
            html.Tr([html.Td("Summary Statistics"), html.Td(), html.Td(), html.Td(),])
        ),
        html.Tbody(
            [
                html.Tr(
                    [
                        html.Td("Mean"),
                        html.Td("", id="stat_tbl_mean"),
                        html.Td("Standard Deviation"),
                        html.Td("", id="stat_tbl_std_dev"),
                    ]
                ),
                html.Tr(
                    [
                        html.Td("Skewness"),
                        html.Td("", id="stat_tbl_skew"),
                        html.Td("Excess Kurtosis"),
                        html.Td("", id="stat_tbl_kurt"),
                    ]
                ),
                # html.Tr([html.Td("Mean"), html.Td("")]),
            ]
        ),
    ],
    hover=True,
    size="sm",
)


@app.callback(
    [
        Output("stat_tbl_mean", "children"),
        Output("stat_tbl_std_dev", "children"),
        Output("stat_tbl_skew", "children"),
        Output("stat_tbl_kurt", "children"),
    ],
    [Input("std_input_tbl", "data")],
)
def update_stats_table(std_rows):
    probs = [float(i["std_probabilities_tbl"]) for i in std_rows]
    pays = [float(i["std_payoffs_tbl"]) for i in std_rows]
    mean_helper = round(sm.mean(pays, probs), 4)
    std_dev_helper = round(sm.std_dev(pays, probs), 4)
    skew_helper = round(sm.skew(pays, probs), 4)
    kurtosis_helper = round(sm.kurtosis(pays, probs), 4)
    return [mean_helper, std_dev_helper, skew_helper, kurtosis_helper]


input_segment = html.Div(
    [
        html.H3(
            html.Strong([html.Span("Input - "), html.Span(id="input_heading")]),
            style=header_style,
            className=header_class,
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                dcc.Dropdown(
                                    id="theor_dropdown",
                                    options=[
                                        {"label": "Expected utility", "value": "EU",},
                                        # {"label": "Rank dependent utility", "value": "RDU",}, # Dont show rdu as it is a subset of CPT
                                        {
                                            "label": "Cumulative prospect theory",
                                            "value": "CPT",
                                        },
                                        {"label": "Regret theory", "value": "RT"},
                                        {"label": "Salience theory", "value": "ST"},
                                        {
                                            "label": "Savoring and Disappointment theory",
                                            "value": "SDT",
                                        },
                                    ],
                                    value="EU",
                                    className="pb-2 d-print-none",
                                ),
                                dbc.Collapse(
                                    # Salience parameter delta here
                                    dbc.Alert(
                                        [
                                            dbc.FormGroup(
                                                [
                                                    dbc.Label(
                                                        "Salience - Local thinking delta:",
                                                        width=6,
                                                        className="my-1",
                                                    ),
                                                    dbc.Col(
                                                        dbc.Input(
                                                            id="sl_delta",
                                                            type="number",
                                                            value=0.5,
                                                            step=0.01,
                                                            min=0,
                                                            max=1,
                                                        ),
                                                        width=6,
                                                    ),
                                                ],
                                                row=True,
                                            ),
                                        ],
                                        color="warning",
                                        className="pb-2",
                                    ),
                                    id="input_sl_collapse",
                                ),
                                dbc.Collapse(
                                    # Savoring parameter delta here
                                    dbc.Alert(
                                        [
                                            dbc.FormGroup(
                                                [
                                                    dbc.Label(
                                                        "Savoring and Disappointment theory - Savoring coefficient:",
                                                        width=6,
                                                        className="my-1",
                                                    ),
                                                    dbc.Col(
                                                        dbc.Input(
                                                            id="sdt_k",
                                                            type="number",
                                                            value=0.5,
                                                            step=0.01,
                                                            min=0,
                                                        ),
                                                        width=6,
                                                    ),
                                                ],
                                                row=True,
                                            ),
                                        ],
                                        color="warning",
                                        className="pb-2",
                                    ),
                                    id="input_sdt_collapse",
                                ),
                                dbc.Collapse(
                                    dbc.FormGroup(
                                        [
                                            dbc.Label("Use a single input:", width=6),
                                            dbc.Col(
                                                daq.BooleanSwitch(
                                                    id="sure_context_bool",
                                                    on=False,
                                                    color=prim_color,
                                                ),
                                                width=6,
                                            ),
                                        ],
                                        row=True,
                                    ),
                                    id="input_sure_context_collapse",
                                    className="d-print-none",
                                ),
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
                                                        "format": FormatTemplate.percentage(
                                                            1
                                                        ),
                                                    },
                                                    {
                                                        "id": "comp_probabilities_tbl",
                                                        "name": "Comp Probabilities",
                                                        "type": "numeric",
                                                        "format": FormatTemplate.percentage(
                                                            1
                                                        ),
                                                    },
                                                    {
                                                        "id": "std_payoffs_tbl",
                                                        "name": "Payoffs",
                                                        "type": "numeric",
                                                    },
                                                    {
                                                        "id": "comp_payoffs_tbl",
                                                        "name": "Comp Payoffs",
                                                        "type": "numeric",
                                                    },
                                                ]
                                            ),
                                            css=[
                                                {
                                                    "selector": ".show-hide",
                                                    "rule": "display: none",
                                                }
                                            ],
                                            style_cell={"textAlign": "center"},
                                            hidden_columns=[
                                                "comp_probabilities_tbl",
                                                "comp_payoffs_tbl",
                                            ],
                                            # style_cell_conditional=[
                                            #     {
                                            #         "if": {
                                            #             "column_id": "std_probabilities_tbl"
                                            #         },
                                            #         "width": "33%",
                                            #     },
                                            #     {
                                            #         "if": {"column_id": "std_payoffs_tbl"},
                                            #         "width": "33%",
                                            #     },
                                            #     {
                                            #         "if": {"column_id": "comp_payoffs_tbl"},
                                            #         "width": "33%",
                                            #     },
                                            # ],
                                            data=[
                                                dict(
                                                    std_probabilities_tbl=0.1,
                                                    comp_probabilities_tbl=0.2,
                                                    std_payoffs_tbl=-1,
                                                    comp_payoffs_tbl=0,
                                                ),
                                                dict(
                                                    std_probabilities_tbl=0.2,
                                                    comp_probabilities_tbl=0.1,
                                                    std_payoffs_tbl=2,
                                                    comp_payoffs_tbl=1,
                                                ),
                                                dict(
                                                    std_probabilities_tbl=0.3,
                                                    comp_probabilities_tbl=0.1,
                                                    std_payoffs_tbl=3,
                                                    comp_payoffs_tbl=4,
                                                ),
                                                dict(
                                                    std_probabilities_tbl=0.2,
                                                    comp_probabilities_tbl=0.2,
                                                    std_payoffs_tbl=5,
                                                    comp_payoffs_tbl=6,
                                                ),
                                                dict(
                                                    std_probabilities_tbl=0.2,
                                                    comp_probabilities_tbl=0.4,
                                                    std_payoffs_tbl=6,
                                                    comp_payoffs_tbl=6,
                                                ),
                                            ],
                                            editable=True,
                                            row_deletable=True,
                                        ),
                                    ],
                                    className="pb-2 px-2 mx-2",
                                ),
                                dbc.Button(
                                    "Add Row",
                                    id="std_editing_rows_button",
                                    n_clicks=0,
                                    className="mb-2 d-print-none",
                                ),
                                # MARK second datatable
                                dbc.Collapse(
                                    [
                                        html.Div(
                                            [
                                                dash_table.DataTable(
                                                    id="add_input_tbl",
                                                    columns=(
                                                        [
                                                            {
                                                                "id": "std_probabilities_tbl",
                                                                "name": "Probabilities",
                                                                "type": "numeric",
                                                                "format": FormatTemplate.percentage(
                                                                    1
                                                                ),
                                                            },
                                                            {
                                                                "id": "std_payoffs_tbl",
                                                                "name": "Payoffs",
                                                                "type": "numeric",
                                                            },
                                                        ]
                                                    ),
                                                    css=[
                                                        {
                                                            "selector": ".show-hide",
                                                            "rule": "display: none",
                                                        }
                                                    ],
                                                    style_cell={"textAlign": "center"},
                                                    data=[
                                                        dict(
                                                            std_probabilities_tbl=1,
                                                            std_payoffs_tbl=-1,
                                                        ),
                                                    ],
                                                    editable=True,
                                                    row_deletable=True,
                                                )
                                            ],
                                            className="pb-2 px-2 mx-2",
                                        ),
                                        dbc.Button(
                                            "Add Row",
                                            id="add_editing_rows_button",
                                            n_clicks=0,
                                            className="mb-2 d-print-none",
                                        ),
                                    ],
                                    id="add_table_collapse",
                                ),
                            ],
                            className="col-4",
                        ),
                        html.Div(
                            [dcc.Graph(id="gamble_figs"), stat_table], className="col",
                        ),
                    ],
                    className="row mt-2",
                ),
                # html.Div(stat_table, className="row m-2"),
            ]
        ),
    ],
    className="p-0 m-0",
)


@app.callback(Output("input_heading", "children"), [Input("theor_dropdown", "value")])
def set_heading(drop_val):
    title = fd.mf_func_dict[drop_val][1]
    return title


# MARK disable choice of pw for certain theories here
@app.callback(
    [
        Output("pw_panel_collapse", "is_open"),
        Output("rg_panel_collapse", "is_open"),
        Output("sl_panel_collapse", "is_open"),
        Output("sdt_panel_collapse", "is_open"),
        Output("input_sl_collapse", "is_open"),
        Output("input_sdt_collapse", "is_open"),
        Output("input_sure_context_collapse", "is_open"),
    ],
    [Input("theor_dropdown", "value")],
)
def collapse_pw(drop_val):
    if drop_val == "EU":
        return False, False, False, False, False, False, False
    elif drop_val == "RT":
        return False, True, False, False, False, False, True
    elif drop_val == "ST":
        return False, False, True, False, True, False, True
    elif drop_val == "SDT":
        return False, False, False, True, False, True, False
    elif drop_val == "CPT":
        return True, False, False, False, False, False, False


# Callbacks for Table
@app.callback(
    [Output("danger_toast_2", "is_open"), Output("danger_toast_2", "children")],
    [Input("std_input_tbl", "data")],
)
def check_probs(rows):
    # Check whether probs in table approximately sum to 1
    probs = [float(i["std_probabilities_tbl"]) for i in rows]
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
    [Output("danger_toast_3", "is_open"), Output("danger_toast_3", "children")],
    [Input("std_input_tbl", "data")],
)
def check_probs(rows):
    # Check whether probs in table approximately sum to 1
    probs = [float(i["comp_probabilities_tbl"]) for i in rows]
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
    [Output("danger_toast_4", "is_open"), Output("danger_toast_4", "children")],
    [Input("add_input_tbl", "data")],
)
def check_probs(rows):
    # Check whether probs in table approximately sum to 1
    probs = [float(i["std_probabilities_tbl"]) for i in rows]
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
    # extend the input table by one empty row per click
    if n_clicks > 0:
        rows.append({c["id"]: "" for c in columns})
    return rows


@app.callback(
    Output("add_input_tbl", "data"),
    [Input("add_editing_rows_button", "n_clicks")],
    [State("add_input_tbl", "data"), State("add_input_tbl", "columns")],
)
def add_row_add_table(n_clicks, rows, columns):
    # extend the input table by one empty row per click
    if n_clicks > 0:
        rows.append({c["id"]: "" for c in columns})
    return rows


@app.callback(
    [
        Output("std_input_tbl", "hidden_columns"),
        Output("add_table_collapse", "is_open"),
    ],
    [Input("theor_dropdown", "value"), Input("sure_context_bool", "on")],
)
def hide_rt_input_column(drop_val, add_context):
    # Hide the rt_input column in which the user can write an alternative lottery to which the target lottery may be compared
    if drop_val in ["RT", "ST"]:
        col_list = ["comp_probabilities_tbl"]
    elif drop_val == "SDT":
        col_list = ["comp_payoffs_tbl"]
    else:
        col_list = ["comp_probabilities_tbl", "comp_payoffs_tbl"]

    if add_context == False:
        add_table_bool = False
    else:
        add_table_bool = True
        col_list = ["comp_probabilities_tbl", "comp_payoffs_tbl"]

    return col_list, add_table_bool


# @app.callback(
#     Output("add_table_collapse", "is_open"), [Input("sure_context_bool", "on")]
# )
# def toggle_add_table(add_context):
#     if add_context == True:
#         return True
#     else:
#         return False


# Manage gamble Figs
@app.callback(
    Output("gamble_figs", "figure"), [Input("std_input_tbl", "data")],
)
def update_gamble_figs(std_rows):
    # Update plots illustrating the lottery entered by the user
    # TODO add logic to display second figs when RT or Salience?
    probs = [float(i["std_probabilities_tbl"]) for i in std_rows]
    pays = [float(i["std_payoffs_tbl"]) for i in std_rows]
    fig = gamble_figs(pays, probs)
    return fig


def gamble_figs(pays, probs):
    # Prepare plots to illustrate the lottery entered by the user
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
    y_1 = [0.5] + list(np.linspace(0, 1, len(list(reversed(probs)))))
    y_2 = [0.25 + 0.5 * i for i in list(np.linspace(0, 1, len(list(reversed(probs)))))]

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
    displ_probs = [f"{round(prob*100, 1)}%" for prob in probs]
    for i in range(len(probs)):
        fig.add_annotation(
            x=0.5,
            y=y_2[i],
            text=list(reversed(displ_probs))[i],
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
            text=list(reversed(pays))[i],
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
        showgrid=False, zeroline=True, tickformat="%", row=1, col=2,
    )

    # Transformation for cdf
    pays_ord, probs_ord = sorted(pays), [x for _, x in sorted(zip(pays, probs))]
    pays_graph = [
        [pays_ord[i], pays_ord[i + 1]]
        if i < len(pays_ord) - 1
        else [pays_ord[i], pays_ord[i] + (pays_ord[i] - pays_ord[0]) * 0.1]
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
                line=dict(color=plot_color, width=4),
            ),
            row=2,
            col=2,
        )

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
        range=[0.0, 1.05], showgrid=False, zeroline=True, tickformat="%", row=2, col=2,
    )
    return fig

