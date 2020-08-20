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

pw_func_dict = {
    "TKW": pw.weigh_tversky_kahneman,
    "GEW": pw.weigh_goldstein_einhorn,
    "PW": pw.weigh_prelec,
}

um_func_dict = {
    "TKU": um.utility_tversky_kahneman,
    "RU": um.root_utility,
    "LU": um.lin_utility,
}

mf_func_dict = {
    "CPT": mf.cumulative_prospect_theory,
    "RDU": mf.rank_dependent_utility,
    "EU": mf.expected_utility,
}

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

input_segment = dbc.Container(
    [
        # TODO sync the two ways of entering data and maybe split them into different tabs
        html.H3("Enter a gamble", className="py-2"),
        dcc.Tabs(
            [
                dcc.Tab(
                    [
                        html.Div(
                            [
                                html.Div(
                                    [
                                        dbc.Button(
                                            "Add Row",
                                            id="editing-rows-button",
                                            n_clicks=0,
                                        ),
                                    ],
                                    className="col-1",
                                ),
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
                                                    payoffs_tbl=1, probabilities_tbl=0.1
                                                ),
                                                dict(
                                                    payoffs_tbl=2, probabilities_tbl=0.4
                                                ),
                                                dict(
                                                    payoffs_tbl=3, probabilities_tbl=0.5
                                                ),
                                            ],
                                            editable=True,
                                            row_deletable=True,
                                        ),
                                    ],
                                    className="col",
                                ),
                            ],
                            className="row my-2",
                        )
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
        dbc.Alert(id="probs_alert", color="warning", is_open=False, dismissable=True,),
        html.Hr(),
    ],
    className="px-2",
)


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
    if sum(probs) != 1:
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
    pays = [i["payoffs_tbl"] for i in rows]
    probs = [i["probabilities_tbl"] for i in rows]
    return pays, probs


# TODO Check wether dash has introduced two way syncing at https://community.plotly.com/t/synchronize-components-bidirectionally/14158
# @app.callback(
#     Output("input_tbl", "data"),
#     [Input("pays_input", "value"), Input("probs_input", "value")],
# )
# def sync_inputs_plain(pays, probs):
#     pays_ls = [float(i) for i in pays.split(",")]
#     probs_ls = [float(i) for i in probs.split(",")]


theor_segment = dbc.Container(
    [
        html.H3("Choose a decision theory", className="py-2",),
        dcc.Dropdown(
            id="theor_dropdown",
            options=[
                {"label": "Cumulative prospect theory", "value": "CPT",},
                {"label": "Rank dependent utility", "value": "RDU",},
                {"label": "Expected utility", "value": "EU",},
            ],
            value="CPT",
        ),
    ],
    className="px-2 pb-2",
)

# MARK disable choice of pw for certain theories here
@app.callback(
    [Output("pw_tab", "disabled"), Output("pw_um_tabs", "value")],
    [Input("theor_dropdown", "value")],
    [State("pw_um_tabs", "value")],
)
def block_pw(drop_val, tab_state):
    if drop_val == "EU":
        return True, "um_tab"
    else:
        return False, tab_state


pw_um_segment = dbc.Container(
    [
        dcc.Tabs(
            [
                dcc.Tab(
                    [
                        html.H3("Utility function", className="py-2",),
                        dcc.Dropdown(
                            id="um_dropdown",
                            options=[
                                {
                                    "label": "Tversky Kahneman utility function",
                                    "value": "TKU",
                                },
                                {"label": "Root utility function", "value": "RU",},
                                {"label": "Linear Utility function", "value": "LU",},
                            ],
                            value="TKU",
                        ),
                        html.Div(
                            [
                                html.Div(
                                    [dcc.Graph(id="um_graph"),], className="col-9",
                                ),
                                html.Div(
                                    [
                                        dbc.Collapse(
                                            [
                                                dbc.Label("a:"),
                                                dbc.Input(
                                                    id="um_TKU_a",
                                                    type="number",
                                                    value=0.88,
                                                    step=0.1,
                                                ),
                                                dbc.Label("l:"),
                                                dbc.Input(
                                                    id="um_TKU_l",
                                                    type="number",
                                                    value=2.25,
                                                    step=0.1,
                                                ),
                                                dbc.Label("r:"),
                                                dbc.Input(
                                                    id="um_TKU_r",
                                                    type="number",
                                                    value=0.0,
                                                    step=1,
                                                ),
                                            ],
                                            id="um_collapse_TKU",
                                        ),
                                        dbc.Collapse(
                                            [
                                                dbc.Label("exp:"),
                                                dbc.Input(
                                                    id="um_RU_exp",
                                                    type="number",
                                                    value=2.0,
                                                    step=1,
                                                ),
                                            ],
                                            id="um_collapse_RU",
                                        ),
                                        dbc.Collapse([], id="um_collapse_LU"),
                                        html.Hr(),
                                        dbc.Label("Minimum display value"),
                                        dbc.Input(
                                            id="um_min_value", type="number", value=0
                                        ),
                                        dbc.Label("Maximum display value"),
                                        dbc.Input(
                                            id="um_max_value", type="number", value=100
                                        ),
                                    ],
                                    className="col",
                                ),
                            ],
                            className="row mt-2",
                        ),
                    ],
                    label="Choose a utility function",
                    value="um_tab",
                    id="um_tab",
                ),
                dcc.Tab(
                    [
                        html.H3("Probability weighting function", className="py-2",),
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
                            ],
                            value="TKW",
                        ),
                        html.Div(
                            [
                                html.Div(
                                    [dcc.Graph(id="pw_graph"),], className="col-9",
                                ),
                                html.Div(
                                    [
                                        dbc.Collapse(
                                            [
                                                dbc.Label("d:"),
                                                dbc.Input(
                                                    id="pw_TKW_d",
                                                    type="number",
                                                    value=0.65,
                                                    step=0.1,
                                                ),
                                            ],
                                            id="pw_collapse_TKW",
                                        ),
                                        dbc.Collapse(
                                            [
                                                dbc.Label("b:"),
                                                dbc.Input(
                                                    id="pw_GEW_b",
                                                    type="number",
                                                    value=0.5,
                                                    min=0,
                                                    max=1,
                                                    step=0.01,
                                                ),
                                                dbc.Label("a:"),
                                                dbc.Input(
                                                    id="pw_GEW_a",
                                                    type="number",
                                                    value=0.6,
                                                    min=0,
                                                    max=1,
                                                    step=0.01,
                                                ),
                                            ],
                                            id="pw_collapse_GEW",
                                        ),
                                        dbc.Collapse(
                                            [
                                                dbc.Label("b:"),
                                                dbc.Input(
                                                    id="pw_PW_b",
                                                    type="number",
                                                    value=0.5,
                                                    min=0,
                                                    max=1,
                                                    step=0.01,
                                                ),
                                                dbc.Label("a:"),
                                                dbc.Input(
                                                    id="pw_PW_a",
                                                    type="number",
                                                    value=0.6,
                                                    min=0,
                                                    max=1,
                                                    step=0.01,
                                                ),
                                            ],
                                            id="pw_collapse_PW",
                                        ),
                                        html.Hr(),
                                        dbc.Label("Minimum display value"),
                                        dbc.Input(
                                            id="pw_min_value",
                                            type="number",
                                            value=0,
                                            min=0,
                                            max=1,
                                            step=0.01,
                                        ),
                                        dbc.Label("Maximum display value"),
                                        dbc.Input(
                                            id="pw_max_value",
                                            type="number",
                                            value=1,
                                            min=0,
                                            max=1,
                                            step=0.01,
                                        ),
                                    ],
                                    className="col",
                                ),
                            ],
                            className="row mt-2",
                        ),
                    ],
                    label="Choose a probability weighting function",
                    value="pw_tab",
                    id="pw_tab",
                ),
            ],
            value="um_tab",
            id="pw_um_tabs",
        )
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
        Input("pw_min_value", "value"),
        Input("pw_max_value", "value"),
        Input("pw_TKW_d", "value"),
        Input("pw_GEW_b", "value"),
        Input("pw_GEW_a", "value"),
        Input("pw_PW_b", "value"),
        Input("pw_PW_a", "value"),
    ],
)
def update_pw_graph(pw_drop_val, min_val, max_val, TKW_d, GEW_b, GEW_a, PW_b, PW_a):
    if pw_drop_val == "TKW":
        kwargs = {"d": TKW_d}
    elif pw_drop_val == "GEW":
        kwargs = {"b": GEW_b, "a": GEW_a}
    elif pw_drop_val == "PW":
        kwargs = {"b": PW_b, "a": PW_a}

    x_1_data = np.linspace(min_val, max_val, 1000)
    y_1_data = [pw_func_dict[pw_drop_val](float(i), **kwargs) for i in x_1_data]

    fig = go.Figure(data=[go.Scatter(x=x_1_data, y=y_1_data)])
    fig.update_layout(
        template="plotly_white", margin=dict(l=25, r=25, b=25, t=25, pad=0),
    )
    return fig


@app.callback(
    [
        Output("um_collapse_TKU", "is_open"),
        Output("um_collapse_RU", "is_open"),
        Output("um_collapse_LU", "is_open"),
    ],
    [Input("um_dropdown", "value")],
    [
        State("um_collapse_TKU", "is_open"),
        State("um_collapse_RU", "is_open"),
        State("um_collapse_LU", "is_open"),
    ],
)
def toggle_um_params(drop_val, TKU_open, RU_open, LU_open):
    TKU_open, RU_open, LU_open = False, False, False
    if drop_val == "TKU":
        TKU_open = True
    elif drop_val == "RU":
        RU_open = True
    elif drop_val == "LU":
        LU_open = True
    return TKU_open, RU_open, LU_open


@app.callback(
    Output("um_graph", "figure"),
    [
        Input("um_dropdown", "value"),
        Input("um_min_value", "value"),
        Input("um_max_value", "value"),
        Input("um_TKU_a", "value"),
        Input("um_TKU_l", "value"),
        Input("um_TKU_r", "value"),
        Input("um_RU_exp", "value"),
    ],
)
def update_um_graph(
    um_drop_val, min_val, max_val, TKU_a, TKU_l, TKU_r, RU_exp,
):
    if um_drop_val == "TKU":
        kwargs = {"a": TKU_a, "l": TKU_l, "r": TKU_r}
    elif um_drop_val == "RU":
        kwargs = {"exp": RU_exp}
    elif um_drop_val == "LU":
        kwargs = {}

    x_1_data = np.linspace(min_val, max_val, 1000)
    y_1_data = [um_func_dict[um_drop_val](float(i), **kwargs) for i in x_1_data]

    fig = go.Figure(data=[go.Scatter(x=x_1_data, y=y_1_data)])
    fig.update_layout(
        template="plotly_white", margin=dict(l=25, r=25, b=25, t=25, pad=0)
    )
    return fig


output_segment = dbc.Container(
    [html.Hr(), html.H3("Output", className="py-2"), html.Div(id="output"),],
    className="px-2",
)


app.layout = html.Div(
    [
        html.Div(
            html.Div(
                dbc.Navbar(
                    [
                        dbc.NavbarBrand(
                            "Risky decisions - Tool", className="ml-5 text-white"
                        ),
                        # dbc.NavItem(dbc.NavLink("Top", href="#")),
                    ],
                    color="dark",
                ),
                className="col-12",
            ),
            className="row",
        ),
        html.Div(
            html.Div(
                [input_segment, theor_segment, pw_um_segment, output_segment,],
                className="col-10",
            ),
            className="row justify-content-md-center mt-2",
        ),
    ]
)


@app.callback(
    Output("output", "children"),
    [
        Input("input_tbl", "data"),
        Input("pays_input", "value"),
        Input("probs_input", "value"),
        Input("data_entry_tab", "value"),
        Input("theor_dropdown", "value"),
        # pw params
        Input("pw_dropdown", "value"),
        Input("pw_TKW_d", "value"),
        Input("pw_GEW_b", "value"),
        Input("pw_GEW_a", "value"),
        Input("pw_PW_b", "value"),
        Input("pw_PW_a", "value"),
        # um params
        Input("um_dropdown", "value"),
        Input("um_TKU_a", "value"),
        Input("um_TKU_l", "value"),
        Input("um_TKU_r", "value"),
        Input("um_RU_exp", "value"),
    ],
)
def update_output(
    rows,
    pays_input,
    probs_input,
    tab_val_entry,
    theor_drop_val,
    # pw params
    pw_drop_val,
    TKW_d,
    GEW_b,
    GEW_a,
    PW_b,
    PW_a,
    # um params
    um_drop_val,
    TKU_a,
    TKU_l,
    TKU_r,
    RU_exp,
):
    if tab_val_entry == "STD":
        probs = [float(i["probabilities_tbl"]) for i in rows]
        pays = [float(i["payoffs_tbl"]) for i in rows]
    elif tab_val_entry == "BLK":
        probs = [float(i) for i in probs_input.split(",")]
        pays = [float(i) for i in pays_input.split(",")]

    # pw params
    if pw_drop_val == "TKW":
        pw_kwargs = {"d": TKW_d}
    elif pw_drop_val == "GEW":
        pw_kwargs = {"b": GEW_b, "a": GEW_a}
    elif pw_drop_val == "PW":
        pw_kwargs = {"b": PW_b, "a": PW_a}
    # um params
    if um_drop_val == "TKU":
        um_kwargs = {"a": TKU_a, "l": TKU_l, "r": TKU_r}
    elif um_drop_val == "RU":
        um_kwargs = {"exp": RU_exp}
    elif um_drop_val == "LU":
        um_kwargs = {}

    if theor_drop_val == "EU":
        res = mf_func_dict[theor_drop_val](
            pays, probs, um_function=um_func_dict[um_drop_val], um_kwargs=um_kwargs,
        )
        return "You used {} to evaluate the gamble with {} as your utility function. This yielded the following outcome: {}.".format(
            theor_drop_val, um_drop_val, res
        )
    else:
        res = mf_func_dict[theor_drop_val](
            pays,
            probs,
            um_function=um_func_dict[um_drop_val],
            pw_function=pw_func_dict[pw_drop_val],
            um_kwargs=um_kwargs,
            pw_kwargs=pw_kwargs,
        )
        return "You used {} to evaluate the gamble with {} as your utility function and {} as your probability weighting function. This yielded the following outcome: {}.".format(
            theor_drop_val, um_drop_val, pw_drop_val, res
        )


if __name__ == "__main__":
    app.run_server(debug=True)
