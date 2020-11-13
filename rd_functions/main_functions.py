import rd_functions.util_mod as um
import rd_functions.prob_weighting as pw
import rd_functions.helpers as he
from typing import List


def regret_theory(
    pays: List[List[float]],
    probs: List[float],
    # MARK need to lookup what this weight parameter is actually supposed to do
    weight: float = 1.0,
    um_function=um.lin_utility,
    um_kwargs={},
) -> float:
    """ Implementation of Regret theory according to Loomes and Sugden 1982; If several gambles are provided, every gamble is evaluated in relation to the weighted average of all other gambles"""
    pays_delta = []
    for i_outer, eval_pay in enumerate(pays):
        comp_pays = [
            pays[i_inner] for i_inner in range(len(pays)) if i_outer != i_inner
        ]
        comp_pays_avg = [sum(x) / len(comp_pays) for x in zip(*comp_pays)]
        pay_delta = [
            regret_theory_interaction(
                eval_pay[i], comp_pays_avg[i], weight, um_function, um_kwargs=um_kwargs
            )
            for i in range(len(eval_pay))
        ]
        pays_delta.append([pay_delta[i] * probs[i] for i in range(len(pay_delta))])
    # print("***********************************")
    # print(pays_delta)
    # print("***********************************")
    ind_vals = [sum(pays) for pays in pays_delta]

    return ind_vals


def regret_theory_interaction(
    x_1, x_2, weight, um_function, um_kwargs={},
):
    """ classic regret function proposed by Loomes and Sugden 1982 """
    return um_function(x_1, **um_kwargs) + weight * (
        um_function(x_1, **um_kwargs) - um_function(x_2, **um_kwargs)
    )


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
