"""Calculate the values and certainty equivalents calculated by the theory of choice under risk chosen by the user and call auxilliary functions

Returns:
    functions: salience theory, regret theory, expected utility theory, rank dependent utility, cumulative prospect theory
"""

import rd_functions.util_mod as um
import rd_functions.prob_weighting as pw
import rd_functions.helpers as he
import rd_functions.context_eval as ce
from typing import List


def salience_theory(
    pays: List[List[float]],
    probs: List[float],
    sl_function=ce.og_salience,
    sl_kwargs={},
    um_function=um.lin_utility,
    um_kwargs={},
    delta: float = 0.7,
    correl_bool: bool = True,
) -> float:
    """Smooth Salience theory as described in the original paper.

    Args:
        pays (List[List[float]]): 2 dim input of payoffs where the first element is the target lottery and the second element the context lottery
        probs (List[float]): 1 or 2 dim input of probs belonging to the payoffs above
        delta (float, optional): degree of local thinking in original model; should be between 0 and 1 where one represents non-local rational thinking. Defaults to 0.5.
        correl_bool (bool, optional): are payoffs correlated i.e. do they share probs or don't they. Defaults to True.

    Returns:
        float: the unique value of the target lottery compared to the context lottery. Might be exteded to certainty equivalent ... later
    """
    if correl_bool:
        pays_prim, pays_cont = pays[0], pays[1]
    # TODO add vals for uncorrelated state spaces
    sal_vals = [
        sl_function(pays_prim[i], pays_cont[i], **sl_kwargs)
        for i in range(len(pays_prim))
    ]
    av_salience = sum(
        [(delta ** (sal_vals[i])) * probs[i] for i in range(len(sal_vals))]
    )
    probs_weights = [
        ((delta ** (-sal_vals[i])) / av_salience) * probs[i] for i in range(len(probs))
    ]
    return sum(
        [
            um_function(pays_prim[i], **um_kwargs) * probs_weights[i]
            for i in range(len(pays_prim))
        ]
    )


# print(salience_theory([[1, 2, 3], [4, 5, 6]], [0.3, 0.4, 0.3]))


def regret_theory(
    pays: List[List[float]],
    probs: List[float],
    um_function=um.lin_utility,
    um_kwargs={},
    rg_function=ce.ls_regret,
    rg_kwargs={},
) -> float:
    """Implementation of Regret theory according to Loomes and Sugden 1982, If several gambles are provided, every gamble is evaluated in relation to the weighted average of all other gambles

    Args:
        pays (List[List[float]]): [description]
        probs (List[float]): [description]
        um_function ([type], optional): utility function applied to individual values. Defaults to um.lin_utility.
        um_kwargs (dict, optional): . Defaults to {}.
        rg_function ([type], optional): regret function used. Defaults to ce.ls_regret.
        rg_kwargs (dict, optional): . Defaults to {}.

    Returns:
        float: unique value of target lottery in relation to context
    """
    pays_delta = []
    for i_outer, eval_pay in enumerate(pays):
        comp_pays = [
            pays[i_inner] for i_inner in range(len(pays)) if i_outer != i_inner
        ]
        comp_pays_avg = [sum(x) / len(comp_pays) for x in zip(*comp_pays)]
        pay_delta = [
            rg_function(
                eval_pay[i],
                comp_pays_avg[i],
                um_function=um_function,
                um_kwargs=um_kwargs,
                **rg_kwargs,
            )
            for i in range(len(eval_pay))
        ]
        pays_delta.append([pay_delta[i] * probs[i] for i in range(len(pay_delta))])
    # print("***********************************")
    # print(pays_delta)
    # print("***********************************")
    ind_vals = [sum(pays) for pays in pays_delta]

    return ind_vals[0]


def expected_utility(
    pays: List[float], probs: List[float], um_function=um.lin_utility, um_kwargs={}
) -> float:
    """
    Takes in two vectors (payoffs and their probability) of numbers of equal length and returns the sum of their product, which is the expected utility.
    """
    pays_ch, probs_ch = he.list_cleaning(pays, probs)
    pays_ch_ut = [um_function(i, **um_kwargs) for i in pays_ch]
    ind_vals = [pays_ch_ut[i] * probs_ch[i] for i in range(len(pays_ch))]
    return sum(ind_vals)


def rank_dependent_utility(
    pays: List[float],
    probs: List[float],
    pw_function=pw.weigh_tversky_kahneman,
    um_function=um.root_utility,
    um_kwargs={},
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
    return sum(ind_vals)


def cumulative_prospect_theory(
    pays: List[float],
    probs: List[float],
    pw_function=pw.weigh_tversky_kahneman,
    um_function=um.utility_tversky_kahneman,
    pw_kwargs={},
    um_kwargs={},
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
    return sum(ind_vals)
