import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

import main_functions as mf

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div(
    children=[
        dbc.Col(
            [
                html.H1(children="Hello Dash"),
                dbc.Container(
                    dbc.Alert("Hello Bootstrap!", color="success"), className="p-5",
                ),
                dbc.Input(
                    id="pays", type="text", placeholder="list of payoffs", debounce=True
                ),
                dbc.Input(
                    id="probs",
                    type="text",
                    placeholder="list of probabilities",
                    debounce=True,
                ),
                html.Div(id="output"),
            ]
        )
    ]
)


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


if __name__ == "__main__":
    app.run_server(debug=True)
