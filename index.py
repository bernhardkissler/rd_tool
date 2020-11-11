import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

from app import app

server = app.server
from apps import input_rd, main_rd, output_rd


navbar = dbc.Navbar(
    [
        dbc.NavbarBrand(
            html.A("Choices under risk - tool", href="#", className="text-white"),
        ),
        dbc.Collapse(
            [
                # FIXME Navbar verdeckt teilweise content, kann der Link offset geändert werden?
                dbc.NavItem(
                    html.A("Utility Link", href="#uf_link", className="text-white"),
                ),
                dbc.NavItem(
                    html.A("Probability Link", href="#pw_link", className="text-white"),
                ),
                dbc.NavItem(
                    html.A("Output Link", href="#output_link", className="text-white"),
                ),
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
        html.Div(html.Div(navbar, className="col-12"), className="row",),
        html.Div(
            html.Div(
                [
                    main_rd.theor_segment,
                    input_rd.input_segment,
                    main_rd.um_segment,
                    main_rd.pw_segment,
                    output_rd.output_segment,
                    main_rd.toast_1,
                    main_rd.toast_2,
                ],
                # FIXME nicht sehr elegantes padding, damit die Navbar nicht den COntent verdeckt
                className="col pt-4 mt-5",
            ),
            className="row justify-content-md-center mt-2",
            style={"background-color": "#F1EEE6"},  # Mamas Favorit #e1eb34
        ),
    ]
)

if __name__ == "__main__":
    # app.run_server(debug=True, port=8080, host="0.0.0.0")
    app.run_server(debug=True)
