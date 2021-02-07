from typing import Container
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

from app import app

server = app.server
from apps import input_rd, main_rd, output_rd
import apps.func_dicts as fd


sub_bg_color = fd.sub_bg_color
prim_color = fd.prim_color


app.layout = html.Div(
    [
        html.Div(
            [
                html.Div(className="col-2 d-sm-none d-md-block d-print-none"),
                html.Div(
                    html.Div(
                        [
                            html.H1(
                                html.Strong("Decisions under Uncertainty"),
                                className="my-4",
                            ),
                            input_rd.input_segment,
                            main_rd.um_segment,
                            main_rd.pw_segment,
                            main_rd.rg_segment,
                            main_rd.sl_segment,
                            main_rd.sdt_segment,
                            main_rd.gl_segment,
                            output_rd.output_segment,
                        ],
                        className="mx-5 py-5",
                    ),
                    className="col my-5 rounded",
                    style={"background-color": sub_bg_color},
                ),
                html.Div(className="col-2 d-none d-md-block d-print-none"),
            ],
            className="row justify-content-md-center",
        ),
        dbc.Container(
            [
                output_rd.ce_toast,
                main_rd.toast_1,
                main_rd.toast_2,
                main_rd.toast_3,
                main_rd.toast_4,
                main_rd.toast_5,
            ],
            style={"position": "fixed", "top": 66, "right": 10, "width": 350,},
        ),
    ],
    style={"background-color": prim_color},  # Mamas Favorit #e1eb34
)

if __name__ == "__main__":
    # app.run_server(debug=True, port=8080, host="0.0.0.0")
    app.run_server(debug=True)
