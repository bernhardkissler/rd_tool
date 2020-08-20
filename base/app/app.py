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

input_segment = dbc.Container(
    [
        # TODO sync the two ways of entering data and maybe split them into different tabs
        html.H3("Inputs", className="py-2"),
        dbc.Label("Payoffs"),
        dbc.Input(
            id="pays", type="text", placeholder="list of payoffs", debounce=True,
        ),
        dbc.Label("Probabilities"),
        dbc.Input(
            id="probs", type="text", placeholder="list of probabilities", debounce=True,
        ),
        dbc.Button("Add Row", id="editing-rows-button", n_clicks=0, className="my-2",),
        dash_table.DataTable(
            id="input_tbl",
            columns=(
                [{"id": "payoffs_tbl", "name": "Payoffs", "type": "numeric",}]
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
    className="px-2",
)


pw_segment = dbc.Container(
    [
        html.H3("Probability weighting function", className="py-2",),
        dcc.Dropdown(
            id="pw_dropdown",
            options=[
                {"label": "Tversky Kahneman weighting function", "value": "TKW",},
                {"label": "Goldstein Einhorn weigting function", "value": "GEW",},
                {"label": "Prelec weighting function", "value": "PW",},
            ],
        ),
        dbc.Collapse(
            [
                dbc.Label("d:"),
                dbc.Input(id="pw_TKW_d", type="number", value=0.65, step=0.1),
            ],
            id="pw_collapse_TKW",
        ),
        dbc.Collapse(
            [
                dbc.Label("b:"),
                dbc.Input(
                    id="pw_GEW_b", type="number", value=0.5, min=0, max=1, step=0.01
                ),
                dbc.Label("a:"),
                dbc.Input(
                    id="pw_GEW_a", type="number", value=0.6, min=0, max=1, step=0.01
                ),
            ],
            id="pw_collapse_GEW",
        ),
        dbc.Collapse(
            [
                dbc.Label("b:"),
                dbc.Input(
                    id="pw_PW_b", type="number", value=0.5, min=0, max=1, step=0.01
                ),
                dbc.Label("a:"),
                dbc.Input(
                    id="pw_PW_a", type="number", value=0.6, min=0, max=1, step=0.01
                ),
            ],
            id="pw_collapse_PW",
        ),
        dcc.Graph(id="pw_graph"),
    ],
    className="px-2",
)


@app.callback(
    [
        Output("pw_collapse_TKW", "is_open"),
        Output("pw_collapse_GEW", "is_open"),
        Output("pw_collapse_PW", "is_open"),
    ],
    [Input("pw_dropdown", "value")],
    [
        State("pw_collapse_TKW", "is_open"),
        State("pw_collapse_GEW", "is_open"),
        State("pw_collapse_PW", "is_open"),
    ],
)
def toggle_pw_params(drop_val, TKW_open, GEW_open, PW_open):
    TKW_open, GEW_open, PW_open = False, False, False
    if drop_val == "TKW":
        TKW_open = True
    elif drop_val == "GEW":
        GEW_open = True
    elif drop_val == "PW":
        PW_open = True
    return TKW_open, GEW_open, PW_open


@app.callback(
    Output("pw_graph", "figure"),
    [
        Input("pw_dropdown", "value"),
        Input("pw_TKW_d", "value"),
        Input("pw_GEW_b", "value"),
        Input("pw_GEW_a", "value"),
        Input("pw_PW_b", "value"),
        Input("pw_PW_a", "value"),
    ],
)
def update_pw_graph(drop_val, TKW_d, GEW_b, GEW_a, PW_b, PW_a):
    if drop_val == "TKW":
        kwargs = {"d": TKW_d}
    elif drop_val == "GEW":
        kwargs = {"b": GEW_b, "a": GEW_a}
    elif drop_val == "PW":
        kwargs = {"b": PW_b, "a": PW_a}

    func_dict = {
        "TKW": pw.weigh_tversky_kahneman,
        "GEW": pw.weigh_goldstein_einhorn,
        "PW": pw.weigh_prelec,
    }
    x_1_data = np.linspace(0, 1, 1000)
    y_1_data = [func_dict[drop_val](float(i), **kwargs) for i in x_1_data]

    return go.Figure(data=[go.Scatter(x=x_1_data, y=y_1_data)])


um_segment = dbc.Container(
    [
        html.H3("Utility function", className="py-2",),
        dcc.Dropdown(
            id="um_dropdown",
            options=[
                {"label": "Tversky Kahneman utility function", "value": "TKU",},
                {"label": "Root utility function", "value": "RU",},
                {"label": "Linear Utility function", "value": "LU",},
            ],
        ),
        dbc.Collapse([], id="um_collapse"),
        dcc.Graph(id="um_graph"),
    ],
    className="px-2",
)

output_segment = dbc.Container(
    [
        html.H3("Output", className="py-2"),
        html.Div(id="output"),
        html.Hr(),
        html.Div(id="output_new"),
    ],
    className="px-2",
)

app.layout = html.Div(
    [
        dbc.Row(
            dbc.Col(
                dbc.Navbar(
                    [
                        dbc.NavbarBrand(
                            "Risky decisions - Tool", className="ml-5 text-white"
                        ),
                        # dbc.NavItem(dbc.NavLink("Top", href="#")),
                    ],
                    color="dark",
                ),
            ),
            className="px-0",
        ),
        dbc.Row(
            dbc.Col(
                [
                    input_segment,
                    html.Hr(),
                    dbc.Row(
                        [
                            # TODO find out how to make these two the same combined width as everything else
                            dbc.Col(pw_segment, width=6, className="px-0",),
                            dbc.Col(um_segment, width=6, className="px-0",),
                        ]
                    ),
                    html.Hr(),
                    output_segment,
                ],
                width=10,
            ),
            justify="center",
            className="px-0",
        ),
    ]
)


# MARK Graphing callbacks


@app.callback(Output("um_graph", "figure"), [Input("um_dropdown", "value")])
def update_pw_graph(selected_pw):
    func_dict = {
        "TKU": um.utility_tversky_kahneman,
        "RU": um.root_utility,
        "LU": um.lin_utility,
    }
    x_1_data = np.linspace(0, 100, 1000)
    y_1_data = [func_dict[selected_pw](float(i)) for i in x_1_data]

    return go.Figure(data=[go.Scatter(x=x_1_data, y=y_1_data)])


# MARK prelim Output functions


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
