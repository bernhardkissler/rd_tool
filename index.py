import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

from app import app

server = app.server
from apps import input_rd, main_rd, output_rd

sub_bg_color = "rgba(255,255,255,1)"
prim_color = "#e3685f"

navbar = dbc.Navbar(
    [
        dbc.NavbarBrand(
            html.A("Choices under risk - tool", href="#", className="text-white"),
        ),
        dbc.Collapse(
            [
                # FIXME Navbar verdeckt teilweise content, kann der Link offset geändert werden?
                # dbc.NavItem(
                #     html.A("Utility Link", href="#uf_link", className="text-white"),
                # ),
                # dbc.NavItem(
                #     html.A("Probability Link", href="#pw_link", className="text-white"),
                # ),
                # dbc.NavItem(
                #     html.A("Output Link", href="#output_link", className="text-white"),
                # ),
            ],
            id="navbar-collapse",
            navbar=True,
        ),
        dbc.NavbarToggler(id="navbar-toggler"),
    ],
    color="dark",
    fixed="top",
)
# add callback for toggling the collapse on small screens
@app.callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [State("navbar-collapse", "is_open")],
)
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


app.layout = html.Div(
    [
        # html.Div(html.Div(navbar, className="col-12"), className="row",),
        html.Div(
            [
                html.Div(className="col-2 d-sm-none d-md-block d-print-none"),
                html.Div(
                    html.Div(
                        [
                            main_rd.theor_segment,
                            input_rd.input_segment,
                            html.Hr(),
                            main_rd.um_segment,
                            main_rd.pw_segment,
                            main_rd.rg_segment,
                            main_rd.sl_segment,
                            html.Hr(),
                            output_rd.output_segment,
                            main_rd.toast_1,
                            main_rd.toast_2,
                        ],
                        className="mx-5 py-5",
                    ),
                    className="col my-5",
                    style={"background-color": sub_bg_color},
                ),
                html.Div(className="col-2 d-none d-md-block d-print-none"),
            ],
            className="row justify-content-md-center",
        ),
    ],
    style={"background-color": prim_color},  # Mamas Favorit #e1eb34
)

if __name__ == "__main__":
    # app.run_server(debug=True, port=8080, host="0.0.0.0")
    app.run_server(debug=True)
