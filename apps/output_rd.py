import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

import plotly.graph_objs as go


# import rd_functions.main_functions as mf
import rd_functions.util_mod as um
import rd_functions.summary_statistics as sm

# import rd_functions.prob_weighting as pw

import apps.func_dicts as fd

plot_color = fd.plot_color
prim_color = fd.prim_color

header_style = {"background-color": prim_color}
header_class = "my-2 p-2 text-white rounded"

from app import app

output_segment = html.Div(
    [
        html.H3(html.Strong("Output"), style=header_style, className=header_class),
        html.Div(id="output_results_params"),
    ],
    className="my-2",
)


@app.callback(
    [Output("output_results_params", "children"), Output("danger_toast_ce", "is_open")],
    [
        Input("std_input_tbl", "data"),
        Input("add_input_tbl", "data"),
        Input("theor_dropdown", "value"),
        Input("sure_context_bool", "on"),
        # pw params
        Input("pw_dropdown", "value"),
        Input("pw_TKW_d", "value"),
        Input("pw_GEW_b", "value"),
        Input("pw_GEW_a", "value"),
        Input("pw_PW_b", "value"),
        Input("pw_PW_a", "value"),
        Input("pw_POW_r", "value"),
        Input("pw_text_runner", "n_clicks"),
        Input("pw_text", "value"),
        # um params
        Input("um_dropdown", "value"),
        Input("um_TKU_a", "value"),
        Input("um_TKU_l", "value"),
        Input("um_TKU_r", "value"),
        Input("um_RU_exp", "value"),
        Input("um_RU_lm", "value"),
        Input("um_BU_a", "value"),
        Input("um_EXU_a", "value"),
        Input("um_text_runner", "n_clicks"),
        Input("um_text", "value"),
        # gl params
        Input("gl_dropdown", "value"),
        Input("gl_TKU_a", "value"),
        Input("gl_TKU_l", "value"),
        Input("gl_TKU_r", "value"),
        Input("gl_RU_exp", "value"),
        Input("gl_RU_lm", "value"),
        Input("gl_BU_a", "value"),
        Input("gl_EXU_a", "value"),
        Input("gl_text_runner", "n_clicks"),
        Input("gl_text", "value"),
        # rg params
        Input("rg_dropdown", "value"),
        Input("rg_LS_weight", "value"),
        Input("rg_text_runner", "n_clicks"),
        Input("rg_text", "value"),
        # sl params
        Input("sl_dropdown", "value"),
        Input("sl_OG_theta", "value"),
        Input("sl_text_runner", "n_clicks"),
        Input("sl_text", "value"),
        Input("sl_delta", "value"),
        # sdt params
        Input("sdt_dropdown", "value"),
        Input("sdt_AH_eta", "value"),
        Input("sdt_k", "value"),
        Input("sdt_text_runner", "n_clicks"),
        Input("sdt_text", "value"),
    ],
)
def update_output(
    rows,
    add_rows,
    theor_drop_val,
    sure_context_bool,
    # pw params
    pw_drop_val,
    TKW_d,
    GEW_b,
    GEW_a,
    PW_b,
    PW_a,
    POW_r,
    pw_n_clicks,
    pw_user_func,
    # um params
    um_drop_val,
    um_TKU_a,
    um_TKU_l,
    um_TKU_r,
    um_RU_exp,
    um_RU_lm,
    um_BU_a,
    um_EXU_a,
    um_n_clicks,
    um_user_func,
    # gl params
    gl_drop_val,
    gl_TKU_a,
    gl_TKU_l,
    gl_TKU_r,
    gl_RU_exp,
    gl_RU_lm,
    gl_BU_a,
    gl_EXU_a,
    gl_n_clicks,
    gl_user_func,
    # rg params
    rg_drop_val,
    LS_weight,
    rg_n_clicks,
    rg_user_func,
    # sl params
    sl_drop_val,
    OG_theta,
    sl_n_clicks,
    sl_user_func,
    sl_delta,
    # sdt params
    sdt_drop_val,
    AH_eta,
    sdt_k,
    sdt_n_clicks,
    sdt_user_func,
):
    if theor_drop_val in ["RT", "ST"]:
        if sure_context_bool:
            pays = [
                [float(i["std_payoffs_tbl"]) for i in rows],
                [float(i["std_payoffs_tbl"]) for i in add_rows],
            ]
            probs = [float(i["std_probabilities_tbl"]) for i in rows]
        else:
            pays = [
                [float(i["std_payoffs_tbl"]) for i in rows],
                [float(i["comp_payoffs_tbl"]) for i in rows],
            ]
            probs = [float(i["std_probabilities_tbl"]) for i in rows]
    elif theor_drop_val == "SDT":
        probs = [
            [float(i["std_probabilities_tbl"]) for i in rows],
            [float(i["comp_probabilities_tbl"]) for i in rows],
        ]
        pays = [float(i["std_payoffs_tbl"]) for i in rows]
    elif theor_drop_val == "RDRA":
        probs = [
            [float(i["std_probabilities_tbl"]) for i in rows],
            [float(i["std_probabilities_tbl"]) for i in add_rows],
        ]
        pays = [
            [float(i["std_payoffs_tbl"]) for i in rows],
            [float(i["std_payoffs_tbl"]) for i in add_rows],
        ]
    else:
        probs = [float(i["std_probabilities_tbl"]) for i in rows]
        pays = [float(i["std_payoffs_tbl"]) for i in rows]

    # calc mean for risk premium
    mean_val = sm.mean(
        [float(i["std_payoffs_tbl"]) for i in rows],
        [float(i["std_probabilities_tbl"]) for i in rows],
    )

    # pw params
    if pw_drop_val == "TKW":
        pw_kwargs = {"d": TKW_d}
    elif pw_drop_val == "GEW":
        pw_kwargs = {"b": GEW_b, "a": GEW_a}
    elif pw_drop_val == "PW":
        pw_kwargs = {"b": PW_b, "a": PW_a}
    elif pw_drop_val == "LW":
        pw_kwargs = {}
    elif pw_drop_val == "POW":
        pw_kwargs = {"r": POW_r}
    elif pw_drop_val == "YW":
        pw_kwargs = {"text": pw_user_func}
    # um params
    if um_drop_val == "TKU":
        um_kwargs = {"a": um_TKU_a, "l": um_TKU_l, "r": um_TKU_r}
    elif um_drop_val == "RU":
        um_kwargs = {"exp": um_RU_exp, "mult": um_RU_lm}
    elif um_drop_val == "LU":
        um_kwargs = {}
    elif um_drop_val == "BU":
        um_kwargs = {"a": um_BU_a}
    elif um_drop_val == "EXU":
        um_kwargs = {"a": um_EXU_a}
    elif um_drop_val == "YU":
        um_kwargs = {"text": um_user_func}
    # gl params
    if gl_drop_val == "TKU":
        gl_kwargs = {"a": gl_TKU_a, "l": gl_TKU_l, "r": gl_TKU_r}
    elif gl_drop_val == "RU":
        gl_kwargs = {"exp": gl_RU_exp, "mult": gl_RU_lm}
    elif gl_drop_val == "LU":
        gl_kwargs = {}
    elif gl_drop_val == "BU":
        gl_kwargs = {"a": gl_BU_a}
    elif gl_drop_val == "EXU":
        gl_kwargs = {"a": gl_EXU_a}
    elif gl_drop_val == "YU":
        gl_kwargs = {"text": gl_user_func}
    # rg params
    if rg_drop_val == "LS":
        rg_kwargs = {"weight": LS_weight}
    elif rg_drop_val == "YR":
        rg_kwargs = {
            "text": rg_user_func,
        }
    # sl params
    if sl_drop_val == "OG":
        sl_kwargs = {"theta": OG_theta}
    elif sl_drop_val == "YS":
        sl_kwargs = {
            "text": sl_user_func,
        }
    # sdt params
    if sdt_drop_val == "AH":
        sdt_kwargs = {"eta": AH_eta}
    elif sdt_drop_val == "YB":
        sdt_kwargs = {
            "text": sdt_user_func,
        }

    if theor_drop_val == "EU":
        res = fd.mf_func_dict[theor_drop_val][0](
            pays,
            probs,
            um_function=fd.um_func_dict[um_drop_val][0],
            um_kwargs=um_kwargs,
            ce_function=fd.um_func_dict[um_drop_val][3],
        )
    elif theor_drop_val == "ST":
        res = fd.mf_func_dict[theor_drop_val][0](
            pays,
            probs,
            um_function=fd.um_func_dict[um_drop_val][0],
            um_kwargs=um_kwargs,
            ce_function=fd.um_func_dict[um_drop_val][3],
            sl_function=fd.sl_func_dict[sl_drop_val][0],
            sl_kwargs=sl_kwargs,
            delta=sl_delta,
        )
    elif theor_drop_val == "RDRA":
        res = fd.mf_func_dict[theor_drop_val][0](
            pays,
            probs,
            um_function=fd.um_func_dict[um_drop_val][0],
            um_kwargs=um_kwargs,
            ce_function=fd.um_func_dict[um_drop_val][3],
            gl_function=fd.um_func_dict[gl_drop_val][0],
            gl_kwargs=gl_kwargs,
        )
    elif theor_drop_val == "RT":
        res = fd.mf_func_dict[theor_drop_val][0](
            pays,
            probs,
            um_function=fd.um_func_dict[um_drop_val][0],
            um_kwargs=um_kwargs,
            ce_function=fd.um_func_dict[um_drop_val][3],
            rg_function=fd.rg_func_dict[rg_drop_val][0],
            rg_kwargs=rg_kwargs,
        )
    elif theor_drop_val == "SDT":
        res = fd.mf_func_dict[theor_drop_val][0](
            pays,
            probs,
            bivu_function=fd.sdt_func_dict[sdt_drop_val][0],
            bivu_kwargs=sdt_kwargs,
            um_function=fd.um_func_dict[um_drop_val][0],
            um_kwargs=um_kwargs,
            ce_function=fd.um_func_dict[um_drop_val][3],
            k=sdt_k,
        )
    else:
        res = fd.mf_func_dict[theor_drop_val][0](
            pays,
            probs,
            um_function=fd.um_func_dict[um_drop_val][0],
            pw_function=fd.pw_func_dict[pw_drop_val][0],
            um_kwargs=um_kwargs,
            ce_function=fd.um_func_dict[um_drop_val][3],
            pw_kwargs=pw_kwargs,
        )

    if fd.um_func_dict[um_drop_val][0] == um.user_utility:
        toast_bool = True
    else:
        toast_bool = False

    if theor_drop_val == "EU":
        intermed_output = None
    elif theor_drop_val == "CPT":
        intermed_output = html.Div(
            [
                html.P(
                    [
                        f"Probability weighting function: {fd.pw_func_dict[pw_drop_val][1]}",
                        html.Br(),
                        html.P(f"Formula: {fd.pw_func_dict[pw_drop_val][2]}"),
                        html.Br(),
                        html.P(f"Parameters: {pw_kwargs}"),
                    ]
                ),
            ]
        )
    elif theor_drop_val == "RT":
        intermed_output = html.Div(
            [
                html.P(
                    [
                        f"Regret function: {fd.rg_func_dict[rg_drop_val][1]}",
                        html.Br(),
                        f"Formula: {fd.rg_func_dict[rg_drop_val][2]}",
                        html.Br(),
                        f"Parameters: {rg_kwargs}",
                    ]
                ),
            ]
        )
    elif theor_drop_val == "ST":
        intermed_output = html.Div(
            [
                html.P(
                    [
                        f"Salience function: {fd.sl_func_dict[sl_drop_val][1]}",
                        html.Br(),
                        f"Formula: {fd.sl_func_dict[sl_drop_val][2]}",
                        html.Br(),
                        f"Parameters: {sl_kwargs}",
                    ]
                ),
            ]
        )
    elif theor_drop_val == "SDT":
        intermed_output = html.Div(
            [
                html.P(
                    [
                        f"Bivariate Utility function: {fd.sdt_func_dict[sdt_drop_val][1]}",
                        html.Br(),
                        f"Formula: {fd.sdt_func_dict[sdt_drop_val][2]}",
                        html.Br(),
                        f"Parameters: {sdt_kwargs}",
                    ]
                ),
            ]
        )
    elif theor_drop_val == "RDRA":
        intermed_output = html.Div(
            [
                html.P(
                    [
                        f"Gain Loss Utility function: {fd.um_func_dict[gl_drop_val][1]}",
                        html.Br(),
                        f"Formula: {fd.um_func_dict[gl_drop_val][2]}",
                        html.Br(),
                        f"Parameters: {gl_kwargs}",
                    ]
                ),
            ]
        )

    output_text = html.Div(
        [
            html.P(
                [
                    f"Payoffs: {pays}",
                    html.Br(),
                    f"Probs: {probs}",
                    html.Br(),
                    f"Chosen Theory: {fd.mf_func_dict[theor_drop_val][1]}",
                ]
            ),
            html.P(
                [
                    f"Utility function: {fd.um_func_dict[um_drop_val][1]}",
                    html.Br(),
                    f"Formula: {fd.um_func_dict[um_drop_val][2]}",
                    html.Br(),
                    f"Parameters: {um_kwargs}",
                ]
            ),
            intermed_output,
            html.P(
                [
                    f"Utility: {round(res[0], 4)}",
                    html.Br(),
                    f"Certainty equivalent: {round(res[1], 4)}",
                    html.Br(),
                    f"Risk Premium: {round(mean_val - res[1], 4)}",
                ]
            ),
        ]
    )

    return output_text, toast_bool


ce_toast = dbc.Toast(
    dcc.Markdown(
        """
        You chose to use a custom utility function. For security reasons, I can't calculate the certainty equivalent and the Risk Premium.
        
        This behavior might be changed in the future.
    """
    ),
    id="danger_toast_ce",
    header="Certainty Equivalent not available.",
    is_open=False,
    dismissable=True,
    icon="danger",
    # style={"position": "fixed", "top": 66, "right": 10, "width": 350},
)
