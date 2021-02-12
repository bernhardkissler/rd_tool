from typing import Container
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import dash_daq as daq


from app import app

server = app.server
from apps import input_rd, main_rd, output_rd, add_info
import apps.func_dicts as fd


sub_bg_color = fd.sub_bg_color
prim_color = fd.prim_color
header_style = {"background-color": prim_color}
header_class = "p-2 text-white rounded"


app.layout = html.Div(
    [
        html.Div(
            [
                html.Div(className="col-2 d-sm-none d-md-block d-print-none"),
                html.Div(
                    html.Div(
                        [
                            html.H1(
                                html.Strong("Decision under risk"), className="my-4",
                            ),
                            dbc.Collapse(
                                [input_rd.input_segment,],
                                id="head_collapse",
                                is_open=True,
                            ),
                            input_rd.stat_sum_segment,
                            dbc.Collapse(
                                [
                                    main_rd.um_segment,
                                    main_rd.pw_segment,
                                    main_rd.rg_segment,
                                    main_rd.sl_segment,
                                    main_rd.sdt_segment,
                                    main_rd.gl_segment,
                                ],
                                id="main_collapse",
                                is_open=True,
                            ),
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
                dbc.Container(
                    [
                        dbc.Row(
                            [
                                dbc.Label("Hide table input:", width=8),
                                dbc.Col(
                                    daq.BooleanSwitch(
                                        id="hide_header_section",
                                        on=False,
                                        color=prim_color,
                                    ),
                                    width=4,
                                    className="mx-0 px-0",
                                ),
                            ],
                            className="align-items-center",
                        ),
                        dbc.Row(
                            [
                                dbc.Label("Hide auxiliary inputs:", width=8),
                                dbc.Col(
                                    daq.BooleanSwitch(
                                        id="hide_main_section",
                                        on=False,
                                        color=prim_color,
                                    ),
                                    width=4,
                                    className="mx-0 px-0",
                                ),
                            ],
                            className="align-items-center",
                        ),
                        dbc.Row(
                            [
                                dbc.Button(
                                    "Show Explanations",
                                    id="add_info_btn",
                                    className="mb-2 mx-3",
                                    # style={"background-color": prim_color},
                                ),
                                dbc.Modal(
                                    [
                                        dbc.ModalHeader(
                                            html.H3(
                                                html.Strong(
                                                    [
                                                        html.Span(
                                                            "Additional Explanations"
                                                        ),
                                                        #  html.Span(id="input_heading")
                                                    ]
                                                ),
                                            ),
                                            style=header_style,
                                            className=header_class,
                                            # className="p-2 text-white rounded",
                                            # style={"background-color": prim_color},
                                        ),
                                        dbc.ModalBody(
                                            add_info.add_info_text,
                                            style={"background-color": sub_bg_color},
                                            className="rounded",
                                        ),
                                        dbc.ModalFooter(
                                            dbc.Button(
                                                "Close",
                                                id="add_info_close_btn",
                                                className="ml-auto",
                                            ),
                                            style={"background-color": prim_color},
                                        ),
                                    ],
                                    id="add_info_modal",
                                    size="xl",
                                    className="b-0",
                                ),
                            ]
                        ),
                        dbc.Row(
                            html.A(
                                "Go to Bachelor Thesis",
                                target="_blank",
                                href="/static/Bachelor_Thesis (6).pdf",
                                className="mx-3 mb-2",
                                style={"text-decoration": "underline"},
                            )
                        ),
                        dbc.Row(
                            html.A(
                                "Go to Source Code",
                                target="_blank",
                                href="https://github.com/bernhardkissler/rd_tool",
                                className="mx-3 mb-2",
                                style={"text-decoration": "underline"},
                            )
                        ),
                    ],
                    style={
                        "position": "fixed",
                        "top": 45,
                        "right": 10,
                        "width": 190,
                        "background-color": "rgba(255,255,255,0.75)",
                    },
                    className="mr-1 rounded align-items-center",
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
                    style={"position": "fixed", "top": 45, "right": 5, "width": 350},
                    # className="mr-0 ",
                ),
            ],
            className="d-print-none",
        ),
    ],
    style={"background-color": prim_color},  # Mamas Favorit #e1eb34
)


@app.callback(
    Output("add_info_modal", "is_open"),
    [Input("add_info_btn", "n_clicks"), Input("add_info_close_btn", "n_clicks")],
    [State("add_info_modal", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


@app.callback(
    Output("main_collapse", "is_open"), [Input("hide_main_section", "on")],
)
def hide_main_section(hide_main_bool):
    if hide_main_bool == True:
        return False
    else:
        return True


@app.callback(
    Output("head_collapse", "is_open"), [Input("hide_header_section", "on")],
)
def hide_header_section(hide_header_bool):
    if hide_header_bool == True:
        return False
    else:
        return True


if __name__ == "__main__":
    # app.run_server(debug=True, port=8080, host="0.0.0.0")
    app.run_server(debug=True)
