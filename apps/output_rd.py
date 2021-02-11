import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

# import plotly.graph_objs as go


# import rd_functions.main_functions as mf
import rd_functions.util_mod as um
import rd_functions.summary_statistics as sm
import rd_functions.main_functions as mf

from math import nan, isnan

# import rd_functions.prob_weighting as pw

import apps.func_dicts as fd

plot_color = fd.plot_color
prim_color = fd.prim_color

header_style = {"background-color": prim_color}
header_class = "my-2 p-2 text-white rounded"

from app import app

output_segment = html.Div(
    [
        html.H3(
            html.Strong("Summary of calculated utilities"),
            style=header_style,
            className=header_class,
        ),
        html.Div(id="output_results_params"),
    ],
    className="my-2",
)


def lot_to_str(pays, probs, cond_div=" | ", state_div="; ", probs_div=": "):
    """convert the pays and probs input in the tool to nicely printable strings

    Args:
        pays (List of Lists): List of pays (remember to put pays of EU and CPT into additional brackets to make them a 2 dimensional list)
        probs (List of Lists): List of probs (remember to put pays of EU and CPT into additional brackets to make them a 2 dimensional list)
        cond_div (Str, optional): Divider between context and target info for pays and probs respectively Defaults to " | ".
        state_div (str, optional): Divider between different outcomes of a lottery. Defaults to "; ".
        probs_div (str, optional): Divider between the pays and probs of a certain outcome. Defaults to ": ".
    """

    def listToString(s):
        str1 = " "
        return str1.join(s)

    if len(pays) == 2 and len(pays[0]) != len(pays[1]):
        pays_str_t = [str(pay) + probs_div for pay in pays[0]]
        probs_str_t = [
            str(probs[0][i]) + state_div if i < len(probs[0]) - 1 else str(probs[0][i])
            for i, _ in enumerate(probs[0])
        ]
        text_el_t = [(pays_str_t[i] + probs_str_t[i]) for i, _ in enumerate(pays_str_t)]
        pays_str_c = [str(pay) + probs_div for pay in pays[1]]
        probs_str_c = [
            str(probs[1][i]) + state_div if i < len(probs[1]) - 1 else str(probs[1][i])
            for i, _ in enumerate(probs[1])
        ]
        text_el_c = [(pays_str_c[i] + probs_str_c[i]) for i, _ in enumerate(pays_str_c)]
        return f"T = ({listToString(text_el_t)}) and C = ({listToString(text_el_c)})"

    elif len(pays) == 2:
        pays_str = [
            str(pays[0][i]) + cond_div + str(pays[1][i]) + probs_div
            for i, _ in enumerate(pays[0])
        ]
    else:
        pays_str = [str(pay) + probs_div for pay in pays[0]]
    if len(probs) == 2:
        probs_str = [
            str(probs[0][i]) + cond_div + str(probs[1][i]) + state_div
            if i < len(probs[0]) - 1
            else str(probs[0][i]) + "|" + str(probs[1][i])
            for i, _ in enumerate(probs[0])
        ]
    else:
        probs_str = [
            str(probs[0][i]) + state_div if i < len(probs[0]) - 1 else str(probs[0][i])
            for i, _ in enumerate(probs[0])
        ]
    text_el = [(pays_str[i] + probs_str[i]) for i, _ in enumerate(pays_str)]
    return f"L = ({listToString(text_el)})"


def dict_print(d):
    """convert a dictionary to a string that can be print nicely

    Args:
        d (dictionary): the dictionary to be printed
    """

    def listToString(s):
        str1 = " "
        return str1.join(s)

    s = []
    counter = 0
    for key, value in d.items():
        counter += 1
        if counter < len(d):
            s.append(f"{key}: {value}; ")
        else:
            s.append(f"{key}: {value}")

    return listToString(s)


@app.callback(
    [
        Output("output_results_params", "children"),
        Output("danger_toast_ce", "is_open"),
        Output("danger_toast_ce", "children"),
    ],
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
    # if theor_drop_val in ["RT", "ST"]:
    if sure_context_bool:
        pays_RT_ST = [
            [float(i["std_payoffs_tbl"]) for i in rows],
            [float(i["std_payoffs_tbl"]) for i in add_rows],
        ]
        probs_RT_ST = [float(i["std_probabilities_tbl"]) for i in rows]
    else:
        pays_RT_ST = [
            [float(i["std_payoffs_tbl"]) for i in rows],
            [float(i["comp_payoffs_tbl"]) for i in rows],
        ]
        probs_RT_ST = [float(i["std_probabilities_tbl"]) for i in rows]
    # elif theor_drop_val == "SDT":
    probs_SDT = [
        [float(i["std_probabilities_tbl"]) for i in rows],
        [float(i["comp_probabilities_tbl"]) for i in rows],
    ]
    pays_SDT = [float(i["std_payoffs_tbl"]) for i in rows]
    # elif theor_drop_val == "RDRA":
    probs_RDRA = [
        [float(i["std_probabilities_tbl"]) for i in rows],
        [float(i["std_probabilities_tbl"]) for i in add_rows],
    ]
    pays_RDRA = [
        [float(i["std_payoffs_tbl"]) for i in rows],
        [float(i["std_payoffs_tbl"]) for i in add_rows],
    ]
    # else:
    probs_EU_CPT = [float(i["std_probabilities_tbl"]) for i in rows]
    pays_EU_CPT = [float(i["std_payoffs_tbl"]) for i in rows]

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

    # calculate generic theory results
    res_eu = mf.expected_utility(pays_EU_CPT, probs_EU_CPT)
    res_cpt = mf.cumulative_prospect_theory(pays_EU_CPT, probs_EU_CPT)
    res_sdt = mf.sav_dis_theory(pays_SDT, probs_SDT)
    res_rdra = mf.RDRA_theory(pays_RDRA, probs_RDRA)
    res_rt = mf.regret_theory(pays_RT_ST, probs_RT_ST)
    res_st = mf.salience_theory(pays_RT_ST, probs_RT_ST,)

    # create RT_ST pretty lottery display
    if sure_context_bool == False:
        RT_ST_lottery = lot_to_str(pays_RT_ST, [probs_RT_ST])
    elif sure_context_bool == True:
        RT_ST_lottery = lot_to_str(pays_RT_ST, [probs_RT_ST, [1]])

    # calculate conditional result
    if theor_drop_val == "EU":
        res = fd.mf_func_dict[theor_drop_val][0](
            pays_EU_CPT,
            probs_EU_CPT,
            um_function=fd.um_func_dict[um_drop_val][0],
            um_kwargs=um_kwargs,
            ce_function=fd.um_func_dict[um_drop_val][3],
        )
        focus_lottery = lot_to_str([pays_EU_CPT], [probs_EU_CPT])
    elif theor_drop_val == "RDRA":
        res = fd.mf_func_dict[theor_drop_val][0](
            pays_RDRA,
            probs_RDRA,
            um_function=fd.um_func_dict[um_drop_val][0],
            um_kwargs=um_kwargs,
            ce_function=fd.um_func_dict[um_drop_val][3],
            gl_function=fd.um_func_dict[gl_drop_val][0],
            gl_kwargs=gl_kwargs,
        )
        focus_lottery = lot_to_str(pays_RDRA, probs_RDRA)
    elif theor_drop_val == "RT":
        res = fd.mf_func_dict[theor_drop_val][0](
            pays_RT_ST,
            probs_RT_ST,
            um_function=fd.um_func_dict[um_drop_val][0],
            um_kwargs=um_kwargs,
            ce_function=fd.um_func_dict[um_drop_val][3],
            rg_function=fd.rg_func_dict[rg_drop_val][0],
            rg_kwargs=rg_kwargs,
        )
        focus_lottery = RT_ST_lottery
    elif theor_drop_val == "ST":
        res = fd.mf_func_dict[theor_drop_val][0](
            pays_RT_ST,
            probs_RT_ST,
            um_function=fd.um_func_dict[um_drop_val][0],
            um_kwargs=um_kwargs,
            ce_function=fd.um_func_dict[um_drop_val][3],
            sl_function=fd.sl_func_dict[sl_drop_val][0],
            sl_kwargs=sl_kwargs,
            delta=sl_delta,
        )
        focus_lottery = RT_ST_lottery
    elif theor_drop_val == "SDT":
        res = fd.mf_func_dict[theor_drop_val][0](
            pays_SDT,
            probs_SDT,
            bivu_function=fd.sdt_func_dict[sdt_drop_val][0],
            bivu_kwargs=sdt_kwargs,
            um_function=fd.um_func_dict[um_drop_val][0],
            um_kwargs=um_kwargs,
            ce_function=fd.um_func_dict[um_drop_val][3],
            k=sdt_k,
        )
        focus_lottery = lot_to_str([pays_SDT], probs_SDT)
    elif theor_drop_val == "CPT":
        res = fd.mf_func_dict[theor_drop_val][0](
            pays_EU_CPT,
            probs_EU_CPT,
            um_function=fd.um_func_dict[um_drop_val][0],
            pw_function=fd.pw_func_dict[pw_drop_val][0],
            um_kwargs=um_kwargs,
            ce_function=fd.um_func_dict[um_drop_val][3],
            pw_kwargs=pw_kwargs,
        )
        res = list(res)
        if pw_drop_val == "YW":
            res[1] = nan
        focus_lottery = lot_to_str([pays_EU_CPT], [probs_EU_CPT])

    if isnan(res[1]) and theor_drop_val == "RDRA":
        toast_bool, toast_text = (
            True,
            "Currently, the calculation of the certainty equivalent is not implemented for this theory.",
        )
    elif isnan(res[1]):
        toast_bool, toast_text = (
            True,
            "You entered a custom function. For security reasons, I can't calculate the certainty equivalent and the Risk Premium.",
        )
    else:
        toast_bool, toast_text = False, ""

    if theor_drop_val == "EU":
        intermed_output = None
    elif theor_drop_val == "CPT":
        intermed_output = html.Div(
            [
                f"Probability weighting function: {fd.pw_func_dict[pw_drop_val][1]}, Parameters: {dict_print(pw_kwargs)}"
            ]
        )
    elif theor_drop_val == "RT":
        intermed_output = html.Div(
            [
                f"Regret function: {fd.rg_func_dict[rg_drop_val][1]}, Parameters: {dict_print(rg_kwargs)}",
            ]
        )
    elif theor_drop_val == "ST":
        intermed_output = html.Div(
            [
                f"Salience function: {fd.sl_func_dict[sl_drop_val][1]}, Parameters: {dict_print(sl_kwargs)}",
            ]
        )
    elif theor_drop_val == "SDT":
        intermed_output = html.Div(
            [
                f"Bivariate Utility function: {fd.sdt_func_dict[sdt_drop_val][1]}, Parameters: {dict_print(sdt_kwargs)}",
            ]
        )
    elif theor_drop_val == "RDRA":
        intermed_output = html.Div(
            [
                f"Gain Loss Utility function: {fd.um_func_dict[gl_drop_val][1]}, Parameters: {dict_print(gl_kwargs)}",
            ]
        )

    tkw_kwargs = {"d": 0.65}
    bu_kwargs = {"a": 0}
    ru_kwargs = {"exp": 2, "mult": "3"}
    lu_kwargs = {}
    tku_kwargs = {"a": 0.88, "l": 2.25}
    og_kwargs = {"theta": 0.1}
    ah_kwargs = {"eta": 0.1}
    ls_kwargs = {"weight": 1}

    if theor_drop_val == "ST":
        focus_name_params = f"{fd.mf_func_dict['ST'][1]}, Parameters: local thinking - $\\delta$: {sl_delta}"
    elif theor_drop_val == "SDT":
        focus_name_params = f"{fd.mf_func_dict['SDT'][1]}, Parameters: savoring coefficient - k: {sdt_k}"
    else:
        focus_name_params = fd.mf_func_dict[theor_drop_val][1]

    output_table = dbc.Table(
        [
            html.Thead(
                html.Tr(
                    [
                        html.Th("Theory name"),
                        html.Th("Lottery"),
                        html.Th("Utility function"),
                        html.Th("Auxiliary function"),
                        html.Th("Utility"),
                        html.Th("Certainty Equivalent"),
                        html.Th("Risk Premium"),
                    ]
                )
            ),
            html.Tbody(
                [
                    html.Tr(
                        [
                            html.Td(focus_name_params),
                            html.Td(focus_lottery),
                            html.Td(
                                f"Utility function: {fd.um_func_dict[um_drop_val][1]}, Parameters: {dict_print(um_kwargs)}"
                            ),
                            html.Td(intermed_output),
                            html.Td(round(res[0], 4)),
                            html.Td(round(res[1], 4) if res[1] != nan else "nan"),
                            html.Td(
                                round(mean_val - res[1], 4) if res[1] != nan else "nan"
                            ),
                        ],
                        style={
                            "color": plot_color,
                            "border": "thin solid" + plot_color,
                        },
                    ),
                    html.Tr(
                        [
                            html.Td(fd.mf_func_dict["EU"][1]),
                            html.Td(lot_to_str([pays_EU_CPT], [probs_EU_CPT])),
                            html.Td(
                                f"Utility function: {fd.um_func_dict['BU'][1]}, Parameters: {dict_print(bu_kwargs)}"
                            ),
                            html.Td(),
                            html.Td(round(res_eu[0], 4),),
                            html.Td(round(res_eu[1], 4),),
                            html.Td(round(mean_val - res_eu[1], 4),),
                        ]
                    ),
                    html.Tr(
                        [
                            html.Td(fd.mf_func_dict["CPT"][1]),
                            html.Td(lot_to_str([pays_EU_CPT], [probs_EU_CPT])),
                            html.Td(
                                f"Utility function: {fd.um_func_dict['TKU'][1]}, Parameters: {dict_print(tku_kwargs)}"
                            ),
                            html.Td(
                                f"Probability weighting function: {fd.pw_func_dict['TKW'][1]}, Parameters: {dict_print(tkw_kwargs)}"
                            ),
                            html.Td(round(res_cpt[0], 4),),
                            html.Td(round(res_cpt[1], 4),),
                            html.Td(round(mean_val - res_cpt[1], 4),),
                        ]
                    ),
                    html.Tr(
                        [
                            html.Td(
                                # CHECK This has to be adjusted manually if SDT standard parameters in main_functions are changed
                                f"{fd.mf_func_dict['SDT'][1]}, Parameters: savoring coefficient - k: 0.5"
                            ),
                            html.Td(lot_to_str([pays_SDT], probs_SDT)),
                            html.Td(
                                f"Utility function: {fd.um_func_dict['RU'][1]}, Parameters: {dict_print(ru_kwargs)}"
                            ),
                            html.Td(
                                f"Bivariate Utility function: {fd.sdt_func_dict['AH'][1]}, Parameters: {dict_print(ah_kwargs)}",
                            ),
                            html.Td(round(res_sdt[0], 4),),
                            html.Td(round(res_sdt[1], 4),),
                            html.Td(round(mean_val - res_sdt[1], 4),),
                        ]
                    ),
                    html.Tr(
                        [
                            html.Td(fd.mf_func_dict["RDRA"][1]),
                            html.Td(lot_to_str(pays_RDRA, probs_RDRA)),
                            html.Td(
                                f"Utility function: {fd.um_func_dict['LU'][1]}, Parameters: {dict_print(lu_kwargs)}"
                            ),
                            html.Td(
                                f"Gain Loss Utility function: {fd.um_func_dict['RU'][1]}, Parameters: {dict_print(ru_kwargs)}",
                            ),
                            html.Td(round(res_rdra[0], 4),),
                            html.Td(round(res_rdra[1], 4),),
                            html.Td(round(mean_val - res_rdra[1], 4),),
                        ]
                    ),
                    html.Tr(
                        [
                            html.Td(fd.mf_func_dict["RT"][1]),
                            html.Td(RT_ST_lottery),
                            html.Td(
                                f"Utility function: {fd.um_func_dict['RU'][1]}, Parameters: {dict_print(ru_kwargs)}"
                            ),
                            html.Td(
                                f"Regret function: {fd.rg_func_dict['LS'][1]}, Parameters: {dict_print(ls_kwargs)}",
                            ),
                            html.Td(round(res_rt[0], 4),),
                            html.Td(round(res_rt[1], 4),),
                            html.Td(round(mean_val - res_rt[1], 4),),
                        ]
                    ),
                    html.Tr(
                        [
                            html.Td(
                                # CHECK This has to be adjusted manually if ST standard parameters in main_functions are changed
                                f"{fd.mf_func_dict['ST'][1]}, Parameters: local thinking - $\\delta$: 0.7"
                            ),
                            html.Td(RT_ST_lottery),
                            html.Td(
                                f"Utility function: {fd.um_func_dict['RU'][1]}, Parameters: {dict_print(ru_kwargs)}"
                            ),
                            html.Td(
                                f"Salience function: {fd.sl_func_dict['OG'][1]}, Parameters: {dict_print(og_kwargs)}",
                            ),
                            html.Td(round(res_st[0], 4),),
                            html.Td(round(res_st[1], 4),),
                            html.Td(round(mean_val - res_st[1], 4),),
                        ]
                    ),
                ]
            ),
        ],
        hover=True,
        size="sm",
    )
    return output_table, toast_bool, toast_text


ce_toast = dbc.Toast(
    # dcc.Markdown(
    #     """
    #     You choos to input a custom function. For security reasons, I can't calculate the certainty equivalent and the Risk Premium.
    # """
    # )
    id="danger_toast_ce",
    header="Certainty Equivalent not available.",
    is_open=False,
    dismissable=True,
    icon="danger",
    # style={"position": "fixed", "top": 66, "right": 10, "width": 350},
)
