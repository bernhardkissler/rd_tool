"""Calculate the values and certainty equivalents calculated by the theory of choice under risk chosen by the user and call auxilliary functions

Returns:
    functions: salience theory, regret theory, expected utility theory, rank dependent utility, cumulative prospect theory
"""

import rd_functions.util_mod as um
import rd_functions.prob_weighting as pw
import rd_functions.helpers as he
import rd_functions.context_eval as ce
from typing import List


def RDRA_theory(
    pays: List[List[float]],
    probs: List[List[float]],
    um_function=um.lin_utility,
    um_kwargs={},
    ce_function=um.lin_ce,
    gl_function=um.lin_utility,
    gl_kwargs={},
) -> float:
    """
    Calculates reference dependend risk attitude - expected utility for a given target lottery and reference lottery of any size
    Use repeatdly to find PPE/CPE in line with RK2007 
    tested against KR 2007
    https://www.experimentalforschung.econ.uni-muenchen.de/studium/veranstaltungsarchiv/b_e_economics/ind_decision_2.pdf

    """

    prim_pays, ref_pays = pays[0], pays[1]
    prim_probs, ref_probs = probs[0], probs[1]

    partial_result = []
    for pay_outer in prim_pays:
        consumption_utility = um_function(pay_outer, **um_kwargs)
        gain_loss_utility = [
            ref_probs[i]
            * gl_function(
                um_function(pay_outer, **um_kwargs)
                - um_function(pay_inner, **um_kwargs),
                **gl_kwargs,
            )
            for i, pay_inner in enumerate(ref_pays)
        ]
        gain_loss_utility = sum(gain_loss_utility)
        partial_result.append(consumption_utility + gain_loss_utility)
    utility = sum(
        [prim_probs[i] * partial_result[i] for i, _ in enumerate(partial_result)]
    )
    # avg_pay_prim = sum([prim_pays[i] * prim_probs[i] for i, _ in enumerate(prim_pays)])
    ce = ce_function(utility, **um_kwargs)
    return utility, ce


def RDRA_wrapper(pays, probs):
    if RDRA_theory([pays[0], pays[0]], [probs[0], probs[0]]) >= RDRA_theory(
        [pays[1], pays[1]], [probs[1], probs[1]]
    ):
        is_CPE = True
    if RDRA_theory([pays[0], pays[0]], [probs[0], probs[0]]) >= RDRA_theory(
        [pays[1], pays[0]], [probs[1], probs[0]]
    ):
        is_PPE = True
    return is_CPE, is_PPE


def sav_dis_theory(
    pays: List[float],
    probs: List[List[float]],
    bivu_function,
    bivu_kwargs={},
    um_function=um.lin_utility,
    um_kwargs={},
    ce_function=um.lin_ce,
    k: float = 0.5,
) -> float:
    """Ex Ante Savoring and Ex Post Disappointment theory by Gollier and Muermann 2010

    Args:
        pays (List[float]): 
        probs (List[List[float]]): 
        bivu_function ([type]): bivariate utility function trading off expected payoff and actual payoff 
        um_function ([type], optional): univariate utility function called in bivu to model deminishing returns... . Defaults to um.lin_utility.
        k (float, optional): weight of Savoring in relation to Ex post disappointment. Typically bigger than zero

    Returns:
        float: The unique value assigned by the theory to a given target lottery in the context of the second theory
    """
    probs_obj, probs_subj = probs[0], probs[1]

    ant_val = ce_function(
        sum(
            [
                um_function(pays[i], **um_kwargs) * probs_subj[i]
                for i, _ in enumerate(probs_subj)
            ]
        ),
        **um_kwargs,
    )
    act_val = sum(
        [
            bivu_function(
                pays[i],
                ant_val,
                um_function=um_function,
                um_kwargs=um_kwargs,
                **bivu_kwargs,
            )
            * probs_obj[i]
            for i in range(len(probs_obj))
        ]
    )
    utility = k * um_function(ant_val, **um_kwargs) + act_val
    ce = ce_function(utility, **um_kwargs)
    return utility, ce


def salience_theory(
    pays: List[List[float]],
    probs: List[float],
    sl_function=ce.og_salience,
    sl_kwargs={},
    um_function=um.lin_utility,
    um_kwargs={},
    ce_function=um.lin_ce,
    delta: float = 0.7,
    correl_bool: bool = True,
) -> float:
    """Smooth Salience theory as described in the original paper.

    Args:
        pays (List[List[float]]): 2 dim input of payoffs where the first element is the target lottery and the second element the context lottery
        probs (List[float]): 1 or 2 dim input of probs belonging to the payoffs above
        delta (float, optional): degree of local thinking in original model; should be between 0 and 1 where one represents non-local rational thinking. Defaults to 0.5.
        correl_bool (bool, optional): are payoffs correlated i.e. do they share probs or don't they. Defaults to True !!! depreciated, correlation is now evaluated based on the length of context_payoffs (i.e., are there more than 1).

    Returns:
        float: the unique value of the target lottery compared to the context lottery. Might be exteded to certainty equivalent ... later
    """
    pays_prim, pays_cont = pays[0], pays[1]

    if len(pays_cont) == 1:
        sal_vals = [
            sl_function(pays_prim[i], pays_cont[0], **sl_kwargs)
            for i in range(len(pays_prim))
        ]
    else:
        sal_vals = [
            sl_function(pays_prim[i], pays_cont[i], **sl_kwargs)
            for i in range(len(pays_prim))
        ]
    av_salience = sum(
        [(delta ** (-sal_vals[i])) * probs[i] for i in range(len(sal_vals))]
    )
    probs_weights = [
        ((delta ** (-sal_vals[i])) / av_salience) * probs[i] for i in range(len(probs))
    ]
    utility = sum(
        [
            um_function(pays_prim[i], **um_kwargs) * probs_weights[i]
            for i in range(len(pays_prim))
        ]
    )
    ce = ce_function(utility, **um_kwargs)
    return utility, ce


# print(salience_theory([[1, 2, 3], [4, 5, 6]], [0.3, 0.4, 0.3]))


def regret_theory(
    pays: List[List[float]],
    probs: List[float],
    um_function=um.lin_utility,
    um_kwargs={},
    ce_function=um.lin_ce,
    rg_function=ce.ls_regret,
    rg_function_ce=ce.ls_regret_ce,
    rg_kwargs={},
) -> float:
    """Implementation of Regret theory according to Loomes and Sugden 1982.

    Args:
        pays (List[List[float]]): Nested list of target and context pays of equal length, where the first sublist are the target pays and the second the context pays.
        probs (List[float]): List of probabilities. Has to be the same length as the target and context pays and sum to 1
        um_function ([type], optional): The utility function applied to individual values. Defaults to um.lin_utility.
        um_kwargs (dict, optional): . Defaults to {}. The arguments used by the utility function
        rg_function ([type], optional): The regret function used. Defaults to ce.ls_regret.
        rg_kwargs (dict, optional): . Defaults to {}. The arguments used by the regret function

    Returns:
            utility: unique value of target lottery in relation to context
            ce: certainty equivalent of the lottery value
    """
    target_pay, context_pay = pays[0], pays[1]

    if len(context_pay) == 1:
        pays_delta = [
            rg_function(
                target_pay[i],
                context_pay[0],
                um_function=um_function,
                um_kwargs=um_kwargs,
                **rg_kwargs,
            )
            for i, _ in enumerate(target_pay)
        ]
    else:
        pays_delta = [
            rg_function(
                target_pay[i],
                context_pay[i],
                um_function=um_function,
                um_kwargs=um_kwargs,
                **rg_kwargs,
            )
            for i, _ in enumerate(target_pay)
        ]
    wavg_pays = sum([pays_delta[i] * probs[i] for i, _ in enumerate(pays_delta)])
    utility = wavg_pays

    if len(context_pay) == 1:
        ce_vals = [
            rg_function_ce(
                utility,
                context_pay[0],
                um_function=um_function,
                um_kwargs=um_kwargs,
                ce_function=ce_function,
                **rg_kwargs,
            )
            for i, _ in enumerate(target_pay)
        ]
    else:
        ce_vals = [
            rg_function_ce(
                utility,
                context_pay[i],
                um_function=um_function,
                um_kwargs=um_kwargs,
                ce_function=ce_function,
                **rg_kwargs,
            )
            for i, _ in enumerate(target_pay)
        ]
    ce = ce_function(
        sum([ce_vals[i] * probs[i] for i, _ in enumerate(ce_vals)]), **um_kwargs
    )
    return utility, ce


def expected_utility(
    pays: List[float],
    probs: List[float],
    um_function=um.lin_utility,
    um_kwargs={},
    ce_function=um.lin_ce,
) -> float:
    """
    Takes in two vectors (payoffs and their probability) of numbers of equal length 
    and returns the sum of their product, which is the expected utility.
    """
    pays_ch, probs_ch = he.list_cleaning(pays, probs)
    pays_ch_ut = [um_function(i, **um_kwargs) for i in pays_ch]
    ind_vals = [pays_ch_ut[i] * probs_ch[i] for i in range(len(pays_ch))]
    utility = sum(ind_vals)
    ce = ce_function(utility, **um_kwargs)
    return utility, ce


# MARK Not utiltized in app
def rank_dependent_utility(
    pays: List[float],
    probs: List[float],
    pw_function=pw.weigh_tversky_kahneman,
    um_function=um.root_utility,
    um_kwargs={},
    ce_function=um.root_ce,
    pw_kwargs={},
) -> float:
    # Sort values by size of payoffs (descending)
    pays_ch, probs_ch = he.list_cleaning(pays, probs)
    vals = list(zip(pays_ch, probs_ch))
    vals.sort(key=lambda elem: elem[0], reverse=True)
    pays_sorted, probs_sorted = zip(*vals)
    pays_sorted_ut = [um_function(i, **um_kwargs) for i in pays_sorted]
    # Calculate marginal decision weights
    decision_weights = []
    for i, _ in enumerate(probs_sorted):
        if i == 0:
            dec_weight = pw_function(sum(probs_sorted[: i + 1]), **pw_kwargs)
            decision_weights.append(dec_weight)
        else:
            dec_weight = pw_function(
                sum(probs_sorted[: i + 1]), **pw_kwargs
            ) - pw_function(sum(probs_sorted[:i]), **pw_kwargs)
            decision_weights.append(dec_weight)
    ind_vals = [
        pays_sorted_ut[i] * decision_weights[i] for i in range(len(pays_sorted_ut))
    ]
    utility = sum(ind_vals)
    ce = ce_function(utility, **um_kwargs)
    return utility, ce


def cumulative_prospect_theory(
    pays: List[float],
    probs: List[float],
    pw_function=pw.weigh_tversky_kahneman,
    um_function=um.utility_tversky_kahneman,
    pw_kwargs={},
    um_kwargs={},
    ce_function=um.ce_tversky_kahneman,
) -> float:
    pays_ch, probs_ch = he.list_cleaning(pays, probs)
    vals = list(zip(pays_ch, probs_ch))
    # split into pos and neg values
    vals_pos = [i for i in vals if i[0] >= 0]
    vals_neg = [i for i in vals if i[0] < 0]
    # zip and order by absolute value
    try:
        vals_pos.sort(key=lambda elem: elem[0], reverse=True)
        pays_sorted_pos, probs_sorted_pos = zip(*vals_pos)
    except:
        pays_sorted_pos, probs_sorted_pos = [], []
    try:
        vals_neg.sort(key=lambda elem: elem[0])
        pays_sorted_neg, probs_sorted_neg = zip(*vals_neg)
    except:
        pays_sorted_neg, probs_sorted_neg = [], []
    # weigh probabilities
    decision_weights_pos = []
    for i, _ in enumerate(probs_sorted_pos):
        if i == 0:
            dec_weight_pos = pw_function(sum(probs_sorted_pos[: i + 1]), **pw_kwargs)
            decision_weights_pos.append(dec_weight_pos)
        else:
            dec_weight_pos = pw_function(
                sum(probs_sorted_pos[: i + 1]), **pw_kwargs
            ) - pw_function(sum(probs_sorted_pos[:i]), **pw_kwargs)
            decision_weights_pos.append(dec_weight_pos)
    decision_weights_neg = []
    for i, _ in enumerate(probs_sorted_neg):
        if i == 0:
            dec_weight_neg = pw_function(sum(probs_sorted_neg[: i + 1]), **pw_kwargs)
            decision_weights_neg.append(dec_weight_neg)
        else:
            dec_weight_neg = pw_function(
                sum(probs_sorted_neg[: i + 1]), **pw_kwargs
            ) - pw_function(sum(probs_sorted_neg[:i]), **pw_kwargs)
            decision_weights_neg.append(dec_weight_neg)
    # collect all outcomes
    probs_final = decision_weights_pos + decision_weights_neg
    # modify utilites
    pays_final = [um_function(i, **um_kwargs) for i in pays_sorted_pos] + [
        um_function(i, **um_kwargs) for i in pays_sorted_neg
    ]
    ind_vals = [pays_final[i] * probs_final[i] for i in range(len(pays_final))]

    utility = sum(ind_vals)
    ce = ce_function(utility, **um_kwargs)
    return utility, ce

