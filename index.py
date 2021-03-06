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
                                dbc.Button(
                                    "Show Explanations",
                                    id="add_info_btn",
                                    className="my-2 mx-3 btn-block",
                                    # style={"background-color": prim_color},
                                ),
                                dbc.Tooltip(
                                    "Show additional explanations for the different sections in this tool in a pop-up.",
                                    target="add_info_btn",
                                ),
                                dbc.Modal(
                                    [
                                        dbc.ModalHeader(
                                            html.H2(html.Strong(["Explanations"]),),
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
                                            className=header_class,
                                            style=header_style,
                                            # style={"background-color": prim_color},
                                        ),
                                    ],
                                    is_open=True,
                                    id="add_info_modal",
                                    size="xl",
                                    className="b-0",
                                ),
                            ]
                        ),
                        html.Hr(),
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
                            id="hide_table_row",
                            className="align-items-center",
                        ),
                        dbc.Tooltip(
                            "Hide the top-most section of the Tool (Theory and Lottery) - This also hides it for printing.",
                            target="hide_table_row",
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
                            id="hide_auxil_row",
                            className="align-items-center",
                        ),
                        html.Hr(),
                        dbc.Tooltip(
                            "Hide all sections between the 'Summary of lotteries and statistics' section and the 'Summary of calculated utilities' section - This also hides it for printing.",
                            target="hide_auxil_row",
                        ),
                        dbc.Row(
                            [
                                html.A(
                                    "Open Bachelor Thesis",
                                    target="_blank",
                                    href="/static/Bachelor_Thesis.pdf",
                                    className="mx-3 mb-2",
                                    style={"text-decoration": "underline"},
                                    id="BT_link",
                                ),
                                dbc.Tooltip(
                                    "Open the most recent version of the Companion Essay in another tab.",
                                    target="BT_link",
                                ),
                            ]
                        ),
                        dbc.Row(
                            [
                                html.A(
                                    "Open Source Code",
                                    target="_blank",
                                    href="https://github.com/bernhardkissler/rd_tool",
                                    className="mx-3 mb-2",
                                    style={"text-decoration": "underline"},
                                    id="SC_link",
                                ),
                                dbc.Tooltip(
                                    "Open the most recent version of the source code for this tool in another tab.",
                                    target="SC_link",
                                ),
                            ]
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
