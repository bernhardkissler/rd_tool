import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import dash_table

import plotly.express as px
import plotly.graph_objs as go

import numpy as np

import main_functions as mf
import util_mod as um
import prob_weighting as pw

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div(
    children=[
        dbc.Navbar(
            dbc.Row(
                [
                    dbc.NavbarBrand(
                        "Risky decisions - Tool", className="ml-5 text-white"
                    ),
                    # dbc.NavItem(dbc.NavLink("Top", href="#")),
                ]
            ),
            # brand="Risky Decisions - Tool",
            # brand_href="#",
            color="dark",
        ),
        dbc.Row(
            children=[
                dbc.Col(
                    [
                        dbc.Container(
                            [
                                html.H3(children="Inputs", className="py-2"),
                                dbc.Label("Payoffs"),
                                dbc.Input(
                                    id="pays",
                                    type="text",
                                    placeholder="list of payoffs",
                                    debounce=True,
                                ),
                                dbc.Label("Probabilities"),
                                dbc.Input(
                                    id="probs",
                                    type="text",
                                    placeholder="list of probabilities",
                                    debounce=True,
                                ),
                                html.Hr(className=""),
                                html.H3(
                                    children="Probability weighting function",
                                    className="py-2",
                                ),
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
                                    ],
                                ),
                                dcc.Graph(id="pw_graph"),
                                html.Hr(className=""),
                                dbc.Button(
                                    "Add Row",
                                    id="editing-rows-button",
                                    n_clicks=0,
                                    className="my-2",
                                ),
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
                                    data=[dict(payoffs_tbl=1, probabilities_tbl=1)],
                                    editable=True,
                                    row_deletable=True,
                                ),
                            ],
                            className="px-1 mx-2",
                        ),
                        dbc.Container(
                            [
                                html.H3(children="Output", className="py-2"),
                                html.Div(id="output"),
                                html.Hr(className=""),
                                html.Div(id="output_new"),
                            ],
                            className="px-1 mx-2",
                        ),
                    ],
                    width=10,
                ),
            ],
            justify="center",
        ),
    ]
)

# MARK Graphin callbacks
@app.callback(Output("pw_graph", "figure"), [Input("pw_dropdown", "value")])
def update_pw_graph(selected_pw):
    x_1_data = np.linspace(0, 1, 1000)
    func_dict = {
        "TKW": pw.weigh_tversky_kahneman,
        "GEW": pw.weigh_goldstein_einhorn,
        "PW": pw.weigh_prelec,
    }
    y_1_data = [func_dict[selected_pw](float(i)) for i in x_1_data]

    return go.Figure(data=[go.Scatter(x=x_1_data, y=y_1_data)])


@app.callback(
    Output("output", "children"), [Input("pays", "value"), Input("probs", "value")],
)
def update_output(input1, input2):
    input1_pr = [float(i) for i in input1.split(",")]
    input2_pr = [float(i) for i in input2.split(",")]

    exp_util = mf.expected_utility(input1_pr, input2_pr)
    cum_pros_theor = mf.cumulative_prospect_theory(input1_pr, input2_pr)

    return "Payoffs {} and Probabilities {} for an expected utility of {} and a CPT value of {}".format(
        input1_pr, input2_pr, exp_util, cum_pros_theor
    )


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
    Output("output_new", "children"),
    [Input("input_tbl", "data"), Input("input_tbl", "columns")],
)
def update_output_new(rows, columns):
    pays = [i["payoffs_tbl"] for i in rows]
    probs = [i["probabilities_tbl"] for i in rows]
    # TODO CHeck what values python reads in from table (sum of inputs was strange before)
    print(pays, probs)
    print(sum(probs))
    exp_util = mf.expected_utility(pays, probs)
    cum_pros_theor = mf.cumulative_prospect_theory(pays, probs)

    return "Payoffs {} and Probabilities {} for an expected utility of {} and a CPT value of {}".format(
        pays, probs, exp_util, cum_pros_theor
    )


if __name__ == "__main__":
    app.run_server(debug=True)
