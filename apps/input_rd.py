# import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

# import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import dash_table
import dash_table.FormatTemplate as FormatTemplate
import dash

import plotly.graph_objs as go
import plotly.express as px
from plotly.subplots import make_subplots
import dash_daq as daq

import apps.func_dicts as fd

plot_color = fd.plot_color
plot_color_sec = fd.plot_color_sec
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
        # html.Thead(
        #     html.Tr([html.Td("Summary Statistics"), html.Td(), html.Td(), html.Td(),])
        # ),
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
    [
        Input("std_input_tbl", "data"),
        Input("add_input_tbl", "data"),
        Input("sure_context_bool", "on"),
        Input("theor_dropdown", "value"),
    ],
)
def update_stats_table(rows, add_rows, sure_context_bool, theor_drop_val):

    # calc mean for risk premium
    # mean_val = sm.mean(
    #     [float(i["std_payoffs_tbl"]) for i in rows],
    #     [float(i["std_probabilities_tbl"]) for i in rows],
    # )

    if theor_drop_val in ["CPT", "EU"]:
        probs = [float(i["std_probabilities_tbl"]) for i in rows]
        pays = [float(i["std_payoffs_tbl"]) for i in rows]
        mean_helper = round(sm.mean(pays, probs), 4)
        std_dev_helper = round(sm.std_dev(pays, probs), 4)
        skew_helper = round(sm.skew(pays, probs), 4)
        kurtosis_helper = round(sm.kurtosis(pays, probs), 4)

        # early return statement
        return [mean_helper, std_dev_helper, skew_helper, kurtosis_helper]

    elif theor_drop_val in ["RT", "ST"]:
        if sure_context_bool:
            pays = [
                [float(i["std_payoffs_tbl"]) for i in rows],
                [float(i["std_payoffs_tbl"]) for i in add_rows],
            ]
            probs = [[float(i["std_probabilities_tbl"]) for i in rows], [1]]
        else:
            pays = [
                [float(i["std_payoffs_tbl"]) for i in rows],
                [float(i["comp_payoffs_tbl"]) for i in rows],
            ]
            probs = [
                [float(i["std_probabilities_tbl"]) for i in rows],
                [float(i["std_probabilities_tbl"]) for i in rows],
            ]
    elif theor_drop_val in ["SDT"]:
        probs = [
            [float(i["std_probabilities_tbl"]) for i in rows],
            [float(i["comp_probabilities_tbl"]) for i in rows],
        ]
        pays = [
            [float(i["std_payoffs_tbl"]) for i in rows],
            [float(i["std_payoffs_tbl"]) for i in rows],
        ]
    elif theor_drop_val == "RDRA":
        probs = [
            [float(i["std_probabilities_tbl"]) for i in rows],
            [float(i["std_probabilities_tbl"]) for i in add_rows],
        ]
        pays = [
            [float(i["std_payoffs_tbl"]) for i in rows],
            [float(i["std_payoffs_tbl"]) for i in add_rows],
        ]

    mean_helper_t = round(sm.mean(pays[0], probs[0]), 4)
    mean_helper_c = round(sm.mean(pays[1], probs[1]), 4)
    mean_helper = f"{mean_helper_t} | {mean_helper_c}"

    std_dev_helper_t = round(sm.std_dev(pays[0], probs[0]), 4)
    std_dev_helper_c = round(sm.std_dev(pays[1], probs[1]), 4)
    std_dev_helper = f"{std_dev_helper_t} | {std_dev_helper_c}"
    try:
        skew_helper_c = round(sm.skew(pays[1], probs[1]), 4)
        skew_helper_t = round(sm.skew(pays[0], probs[0]), 4)
        skew_helper = f"{skew_helper_t} | {skew_helper_c}"

        kurtosis_helper_c = round(sm.kurtosis(pays[1], probs[1]), 4)
        kurtosis_helper_t = round(sm.kurtosis(pays[0], probs[0]), 4)
        kurtosis_helper = f"{kurtosis_helper_t} | {kurtosis_helper_c}"
    except:
        skew_helper = f"{round(sm.skew(pays[0], probs[0]), 4)} | na"
        kurtosis_helper = f"{round(sm.kurtosis(pays[0], probs[0]), 4)} | na"

    return [mean_helper, std_dev_helper, skew_helper, kurtosis_helper]


stat_sum_segment = html.Div(
    [
        html.H3(
            html.Strong(
                [
                    html.Span("Summary of lotteries and statistics"),
                    #  html.Span(id="input_heading")
                ]
            ),
            style=header_style,
            className=header_class,
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            [dcc.Graph(id="gamble_figs", className="pb-2"), stat_table],
                            className="col",
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


# Manage gamble Figs
@app.callback(
    Output("gamble_figs", "figure"),
    [
        Input("std_input_tbl", "data"),
        Input("add_input_tbl", "data"),
        Input("theor_dropdown", "value"),
        Input("sure_context_bool", "on"),
    ],
)
def update_gamble_figs(std_rows, add_rows, theor_drop_val, sure_context_bool):
    # Update plots illustrating the lottery entered by the user
    probs = [float(i["std_probabilities_tbl"]) for i in std_rows]
    pays = [float(i["std_payoffs_tbl"]) for i in std_rows]
    if theor_drop_val in ["SDT"]:
        probs_comp = [float(i["comp_probabilities_tbl"]) for i in std_rows]
    elif theor_drop_val in ["RT", "ST"] and sure_context_bool == False:
        pays_comp = [float(i["comp_payoffs_tbl"]) for i in std_rows]
    elif (theor_drop_val in ["RT", "ST"] and sure_context_bool == True) or (
        theor_drop_val in ["RDRA"]
    ):
        probs_add = [float(i["std_probabilities_tbl"]) for i in add_rows]
        pays_add = [float(i["std_payoffs_tbl"]) for i in add_rows]

    # Prepare plots to illustrate the lottery entered by the user
    fig = make_subplots(
        rows=2,
        cols=2,
        specs=[[{"rowspan": 2}, {}], [None, {}]],
        shared_xaxes=True,
        subplot_titles=(
            "Lotteries",
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
    # prim_lottery
    if len(probs) > 1:
        y_1 = [0.5] + list(np.linspace(0, 1, len(list(reversed(probs)))))
    else:
        y_1 = [0.5, 0.5]
    y_2 = [
        0.25 + 0.5 * i if len(probs) > 1 else 0.5
        for i in list(np.linspace(0, 1, len(list(reversed(probs)))))
    ]

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

    if theor_drop_val == "SDT":
        displ_probs = [
            f"{round(probs[i]*100, 1)}% | {round(probs_comp[i]*100, 1)}%"
            for i, _ in enumerate(probs)
        ]
    else:
        displ_probs = [f"{round(probs[i]*100, 1)}%" for i, _ in enumerate(probs)]

    textangle = [(y - 0.5) * -90 if y > 0.5 else (0.5 - y) * 90 for y in y_2]

    for i in range(len(probs)):
        fig.add_annotation(
            x=0.5,
            y=y_2[i],
            text=list(reversed(displ_probs))[i],
            ax=0,
            ay=-10,
            arrowcolor="rgba(0,0,0,0)",
            row=1,
            col=1,
            textangle=textangle[i],
        )

    if (theor_drop_val in ["ST", "RT"]) and (sure_context_bool == False):
        displ_pays = [f"{pays[i]} | {pays_comp[i]}" for i, _ in enumerate(pays)]
    elif theor_drop_val in ["ST", "RT"] and (sure_context_bool == True):
        displ_pays = [f"{pays[i]} | {pays_add[0]}" for i, _ in enumerate(pays)]
    else:
        displ_pays = [f"{pays[i]}" for i, _ in enumerate(pays)]
    for i in range(len(probs)):
        fig.add_annotation(
            x=1,
            y=y_1[i + 1],
            text=list(reversed(displ_pays))[i],
            xanchor="left",
            ax=5,
            ay=0,
            arrowcolor="rgba(0,0,0,0)",
            row=1,
            col=1,
        )
    # draw Name
    # fig.add_annotation(
    #     x=0, y=0.5, xanchor="right", text="L", ax=-5, ay=0, arrowcolor="rgba(0,0,0,0)",
    # )
    fig.update_xaxes(
        # range=[-0.4, 1.4],
        showgrid=False,
        zeroline=False,
        visible=False,
        row=1,
        col=1,
    )
    fig.update_yaxes(
        # range=[-0.1, 1.1],
        showgrid=False,
        zeroline=False,
        visible=False,
        scaleanchor="x",
        scaleratio=1,
        row=1,
        col=1,
    )

    # draw context_tree
    if theor_drop_val in ["RDRA"]:
        probs_c = probs_add
        pays_c = pays_add

        if len(probs_c) > 1:
            y_c_1 = [0.5] + list(np.linspace(0, 1, len(list(reversed(probs_c)))))
        else:
            y_c_1 = [0.5, 0.5]
        y_c_2 = [
            0.25 + 0.5 * i if len(probs_c) > 1 else 0.5
            for i in list(np.linspace(0, 1, len(list(reversed(probs_c)))))
        ]
        y_c_1 = [-obj for obj in y_c_1]
        y_c_2 = [-obj for obj in y_c_2]

        for i in range(len(probs_c)):
            fig.add_trace(
                go.Scatter(
                    x=[0, 1],
                    y=[-0.5 - 0.5, y_c_1[i + 1] - 0.5],  # pot fehler hier
                    mode="lines",
                    line=dict(color=plot_color),
                    marker=dict(color=plot_color),
                    hoverinfo="none",
                ),
                row=1,
                col=1,
            )
        displ_probs_c = [f"{round(probs_c[i]*100, 1)}%" for i, _ in enumerate(probs_c)]
        textangle_c = [(-y - 0.5) * 90 if y > 0.5 else (0.5 + y) * -90 for y in y_c_2]

        for i in range(len(probs_c)):
            fig.add_annotation(
                x=0.5,
                y=y_c_2[i] - 0.5,
                text=list(reversed(displ_probs_c))[i],
                ax=0,
                ay=-10,
                arrowcolor="rgba(0,0,0,0)",
                row=1,
                col=1,
                textangle=textangle_c[i],
            )

        displ_pays_c = [f"{pays_c[i]}" for i, _ in enumerate(pays_c)]
        for i in range(len(probs_c)):
            fig.add_annotation(
                x=1,
                y=y_c_1[i + 1] - 0.5,
                text=list(reversed(displ_pays_c))[i],
                xanchor="left",
                ax=5,
                ay=0,
                arrowcolor="rgba(0,0,0,0)",
                row=1,
                col=1,
            )

    # PDF Figure Trace
    fig.add_trace(go.Bar(x=pays, y=probs, marker_color=plot_color), row=1, col=2)
    if theor_drop_val in ["RT", "ST"]:
        if sure_context_bool == False:
            fig.add_trace(
                go.Bar(x=pays_comp, y=probs, marker_color=plot_color_sec), row=1, col=2
            )
        else:
            fig.add_trace(
                go.Bar(x=pays_add, y=probs_add, marker_color=plot_color_sec),
                row=1,
                col=2,
            )
    elif theor_drop_val in ["SDT"]:
        # if sure_context_bool == False:
        fig.add_trace(
            go.Bar(x=pays, y=probs_comp, marker_color=plot_color_sec), row=1, col=2
        )
        # CHECK, kann das hier eigentlich eintreten?
        # else:
        #     fig.add_trace(
        #         go.Bar(x=pays_add, y=probs_add, marker_color=plot_color_sec),
        #         row=1,
        #         col=2,
        #     )
    elif theor_drop_val in ["RDRA"]:
        fig.add_trace(
            go.Bar(x=pays_add, y=probs_add, marker_color=plot_color_sec), row=1, col=2
        )

    if theor_drop_val in ["ST", "RT"]:
        if sure_context_bool == False:
            tick_pays = pays + pays_comp
        else:
            tick_pays = pays + pays_add
    else:
        if theor_drop_val == "RDRA":
            tick_pays = pays + pays_add
        else:
            tick_pays = pays
    fig.update_xaxes(
        showgrid=False,
        zeroline=False,
        visible=True,
        tickmode="array",
        tickvals=tick_pays,
        row=1,
        col=2,
    )
    fig.update_yaxes(
        showgrid=False, zeroline=True, tickformat="%", row=1, col=2,
    )

    # Transformation for cdf
    # prim lottery
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

    # comp_lottery
    if (theor_drop_val == "RDRA") or (
        (theor_drop_val in ["RT", "ST"]) and (sure_context_bool == True)
    ):
        pays_add_ord, probs_add_ord = (
            sorted(pays_add),
            [x for _, x in sorted(zip(pays_add, probs_add))],
        )
        pays_graph_add = [
            [pays_add_ord[i], pays_add_ord[i + 1]]
            if i < len(pays_add_ord) - 1
            else [
                pays_add_ord[i],
                pays_add_ord[i] + (pays_add_ord[i] - pays_add_ord[0]) * 0.1,
            ]
            for i in range(len(pays_add_ord))
        ]
        probs_add_graph = [
            2 * [sum(probs_add_ord[: i + 1])] if i < len(probs_add_ord) else 2 * []
            for i in range(len(probs_add_ord))
        ]
        for i, _ in enumerate(pays_graph_add):
            fig.add_trace(
                go.Scatter(
                    x=pays_graph_add[i],
                    y=probs_add_graph[i],
                    mode="lines",
                    line=dict(color=plot_color_sec, width=4, dash="dot"),
                ),
                row=2,
                col=2,
            )
    elif theor_drop_val in ["RT", "ST"]:
        pays_comp_ord = sorted(pays_comp)
        pays_comp_graph = [
            [pays_comp_ord[i], pays_comp_ord[i + 1]]
            if i < len(pays_comp_ord) - 1
            else [
                pays_comp_ord[i],
                pays_comp_ord[i] + (pays_comp_ord[i] - pays_comp_ord[0]) * 0.1,
            ]
            for i in range(len(pays_comp_ord))
        ]

        for i, _ in enumerate(pays_comp_graph):
            fig.add_trace(
                go.Scatter(
                    x=pays_comp_graph[i],
                    y=probs_graph[i],
                    mode="lines",
                    line=dict(color=plot_color_sec, width=4, dash="dot"),
                ),
                row=2,
                col=2,
            )
    elif theor_drop_val == "SDT":
        probs_comp_ord = [x for _, x in sorted(zip(pays, probs_comp))]
        probs_comp_graph = [
            2 * [sum(probs_comp_ord[: i + 1])] if i < len(probs_comp_ord) else 2 * []
            for i in range(len(probs_comp_ord))
        ]
        for i, _ in enumerate(pays_graph):
            fig.add_trace(
                go.Scatter(
                    x=pays_graph[i],
                    y=probs_comp_graph[i],
                    mode="lines",
                    line=dict(color=plot_color_sec, width=4, dash="dot"),
                ),
                row=2,
                col=2,
            )

    fig.update_xaxes(
        showgrid=False,
        zeroline=False,
        visible=True,
        tickmode="array",
        tickvals=tick_pays,
        row=2,
        col=2,
    )
    fig.update_yaxes(
        range=[0.0, 1.05], showgrid=False, zeroline=True, tickformat="%", row=2, col=2,
    )
    return fig


input_segment = html.Div(
    [
        html.H3(
            html.Strong(
                [
                    html.Span("Theory ("),
                    html.Span(id="input_heading"),
                    html.Span(") and Lottery"),
                ]
            ),
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
                                        {
                                            "label": "Optimal Anticipation with Savoring and Disappointment",
                                            "value": "SDT",
                                        },
                                        {
                                            "label": "Reference Dependent Risk Attitudes",
                                            "value": "RDRA",
                                        },
                                        {"label": "Regret theory", "value": "RT"},
                                        {"label": "Salience theory", "value": "ST"},
                                    ],
                                    searchable=False,
                                    clearable=False,
                                    value="EU",
                                    className="pb-2 d-print-none",
                                ),
                                dbc.Tooltip(
                                    "Choose a theory of choice under risk to adjsut its parameters and functional form and see the outcome in the last section.",
                                    target="theor_dropdown",
                                ),
                                html.Div(
                                    [
                                        dash_table.DataTable(
                                            id="std_input_tbl",
                                            columns=(
                                                [
                                                    {
                                                        "id": "std_probabilities_tbl",
                                                        "name": "Target probabilities",
                                                        "type": "numeric",
                                                        "format": FormatTemplate.percentage(
                                                            1
                                                        ),
                                                    },
                                                    {
                                                        "id": "comp_probabilities_tbl",
                                                        "name": "Context probabilities",
                                                        "type": "numeric",
                                                        "format": FormatTemplate.percentage(
                                                            1
                                                        ),
                                                    },
                                                    {
                                                        "id": "std_payoffs_tbl",
                                                        "name": "Target payoffs",
                                                        "type": "numeric",
                                                    },
                                                    {
                                                        "id": "comp_payoffs_tbl",
                                                        "name": "Context payoffs",
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
                                                    std_payoffs_tbl=1,
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
                                dbc.Tooltip(
                                    "Add another row to the above input table. Rows can be removed by clicking the x in the left-most column.",
                                    target="std_editing_rows_button",
                                ),
                            ],
                            className="col",
                        ),
                        html.Div(
                            [
                                dbc.Collapse(
                                    # Salience parameter delta here
                                    # dbc.Alert(
                                    [
                                        dbc.FormGroup(
                                            [
                                                dbc.Label(
                                                    "Local thinking - delta:",
                                                    width=6,
                                                    className="my-1",
                                                ),
                                                dbc.Col(
                                                    dbc.Input(
                                                        id="sl_delta",
                                                        type="number",
                                                        value=0.7,
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
                                    #     color="warning",
                                    #     className="pb-2",
                                    # ),
                                    id="input_sl_collapse",
                                ),
                                dbc.Collapse(
                                    # Savoring parameter delta here
                                    # dbc.Alert(
                                    [
                                        dbc.FormGroup(
                                            [
                                                dbc.Label(
                                                    "Savoring coefficient - k:",
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
                                    #     color="warning",
                                    #     className="pb-2",
                                    # ),
                                    id="input_sdt_collapse",
                                ),
                                dbc.Collapse(
                                    [
                                        dbc.FormGroup(
                                            [
                                                dbc.Label(
                                                    "Use a single input:", width=6
                                                ),
                                                dbc.Col(
                                                    daq.BooleanSwitch(
                                                        id="sure_context_bool",
                                                        on=False,
                                                        color=prim_color,
                                                    ),
                                                    width=6,
                                                ),
                                            ],
                                            id="sure_context_row",
                                            row=True,
                                        ),
                                        dbc.Tooltip(
                                            "This switch allows you to enter a sure payoff to which the target lottery is compared for Regret theory and Salience theory rather than entering the correlated payoffs in the table on the left.",
                                            target="sure_context_row",
                                        ),
                                    ],
                                    id="input_sure_context_collapse",
                                    className="d-print-none",
                                ),
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
                                                                "name": "Context probabilities",
                                                                "type": "numeric",
                                                                "format": FormatTemplate.percentage(
                                                                    1
                                                                ),
                                                            },
                                                            {
                                                                "id": "std_payoffs_tbl",
                                                                "name": "Context payoffs",
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
                                        html.Div(
                                            [
                                                dbc.Button(
                                                    "Add Row",
                                                    id="add_editing_rows_button",
                                                    n_clicks=0,
                                                    className="mb-2 d-print-none",
                                                ),
                                                dbc.Tooltip(
                                                    "Add another row to the above input table. Rows can be removed by clicking the x in the left-most column.",
                                                    target="add_editing_rows_button",
                                                ),
                                            ],
                                            id="add_table_add_row_button",
                                        ),
                                    ],
                                    id="add_table_collapse",
                                ),
                            ],
                            className="col",
                        ),
                    ],
                    className="row mt-2",
                ),
            ]
        ),
    ],
    className="p-0 m-0",
)


@app.callback(
    Output("sure_context_bool", "on"),
    [Input("theor_dropdown", "value")],
    [State("sure_context_bool", "on")],
)
def reset_add_table_bool(drop_val, sure_context_bool_cur):
    if drop_val in ["EU", "CPT", "SDT", "RDRA"]:
        sure_context_bool = False
    else:
        sure_context_bool = sure_context_bool_cur
    return sure_context_bool


@app.callback(
    Output("um_dropdown", "value"),
    [Input("theor_dropdown", "value")],
    [State("um_dropdown", "value")],
)
def set_sens_default_functions(drop_val, cur_func_um):
    if drop_val in ["CPT"]:
        default_um = "TKU"
    elif drop_val in ["RDRA"]:
        default_um = "LU"
    elif drop_val in ["SDT", "RT", "ST"]:
        default_um = "RU"
    else:
        default_um = cur_func_um
    return default_um


@app.callback(Output("input_heading", "children"), [Input("theor_dropdown", "value")])
def set_heading(drop_val):
    title = fd.mf_func_dict[drop_val][1]
    return title


@app.callback(
    [
        Output("pw_panel_collapse", "is_open"),
        Output("rg_panel_collapse", "is_open"),
        Output("sl_panel_collapse", "is_open"),
        Output("sdt_panel_collapse", "is_open"),
        Output("input_sl_collapse", "is_open"),
        Output("input_sdt_collapse", "is_open"),
        Output("gl_panel_collapse", "is_open"),
        Output("input_sure_context_collapse", "is_open"),
    ],
    [Input("theor_dropdown", "value")],
)
def collapse_pw(drop_val):
    if drop_val == "EU":
        return False, False, False, False, False, False, False, False
    elif drop_val == "RDRA":
        return False, False, False, False, False, False, True, False
    elif drop_val == "RT":
        return False, True, False, False, False, False, False, True
    elif drop_val == "ST":
        return False, False, True, False, True, False, False, True
    elif drop_val == "SDT":
        return False, False, False, True, False, True, False, False
    elif drop_val == "CPT":
        return True, False, False, False, False, False, False, False


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
    [Input("std_input_tbl", "data"), Input("theor_dropdown", "value"),],
)
def check_probs(rows, drop_val):
    # Check whether probs in table approximately sum to 1
    if drop_val in ["SDT"]:
        probs = [float(i["comp_probabilities_tbl"]) for i in rows]
        if not isclose(sum(probs), 1):
            return (
                True,
                "Please make sure that the anticipated probabilities of the different payoffs add to 1. In the moment their sum is {}.".format(
                    sum(probs)
                ),
            )
        else:
            return False, ""
    else:
        return False, ""


@app.callback(
    [Output("danger_toast_4", "is_open"), Output("danger_toast_4", "children")],
    [
        Input("add_input_tbl", "data"),
        Input("theor_dropdown", "value"),
        Input("sure_context_bool", "on"),
    ],
)
def check_probs(rows, drop_val, add_context):
    # Check whether probs in table approximately sum to 1
    probs = [float(i["std_probabilities_tbl"]) for i in rows]
    if not isclose(sum(probs), 1) and (
        (drop_val in ["RT", "ST"] and add_context == True) or drop_val in ["RDRA"]
    ):
        return (
            True,
            "Please make sure that the probabilities of the different payoffs in the bottom table add to 1. In the moment their sum is {}.".format(
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
    [Output("add_input_tbl", "data"), Output("add_table_add_row_button", "style")],
    [
        Input("add_editing_rows_button", "n_clicks"),
        Input("sure_context_bool", "on"),
        Input("theor_dropdown", "value"),
    ],
    [State("add_input_tbl", "data"), State("add_input_tbl", "columns")],
)
def add_row_add_table(n_clicks, sure_context, theor_dropdown, rows, columns):
    # extend the input table by one empty row per click
    if theor_dropdown in ["RT", "ST"] and sure_context == True:
        rows = [{"std_probabilities_tbl": 1, "std_payoffs_tbl": -1}]
        button_diplay = {"display": "none"}
    else:
        ctx = dash.callback_context
        if (
            ctx.triggered[0]["prop_id"] == "add_editing_rows_button.n_clicks"
            and n_clicks > 0
        ):
            rows.append({c["id"]: "" for c in columns})
        button_diplay = {"diplay": "inline"}
    return rows, button_diplay


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

    if drop_val == "RDRA":
        add_table_bool = True

    return col_list, add_table_bool

