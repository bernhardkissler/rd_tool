import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

from app import app
from apps import input_rd, main_rd, output_rd

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
                [
                    main_rd.theor_segment,
                    input_rd.input_segment,
                    main_rd.pw_um_segment,
                    output_rd.output_segment,
                    main_rd.toast_1,
                    main_rd.toast_2
                ],
                className="col-10",
            ),
            className="row justify-content-md-center mt-2",
        ),
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)
