import util_mod as um
import prob_weighting as pw
import helpers as he


def expected_utility(pays, probs, util_function=um.root_utility):
    """
    Takes in two vectors (payoffs and their probability) of numbers of equal length and returns the sum of their product, which is the expected utility.
    """
    # TODO improve documentation of the function (how to give more information on the parameters)
    pays_ch, probs_ch = he.list_cleaning(pays, probs)
    pays_ch_ut = [util_function(i) for i in pays_ch]
    ind_vals = [pays_ch_ut[i] * probs_ch[i] for i in range(len(pays_ch))]
    return sum(ind_vals)


def rank_dependent_utility(pays, probs, d=0.65, util_function=um.root_utility):
    # Sort values by size of payoffs (descending)
    pays_ch, probs_ch = he.list_cleaning(pays, probs)
    vals = list(zip(pays_ch, probs_ch))
    vals.sort(key=lambda elem: elem[0], reverse=True)
    pays_sorted, probs_sorted = zip(*vals)
    pays_sorted_ut = [util_function(i) for i in pays_sorted]
    # Calculate marginal decision weights
    decision_weights = []
    for i, _ in enumerate(probs_sorted):
        if i == 0:
            dec_weight = pw.weigh_tversky_kahneman(sum(probs_sorted[: i + 1]), d)
            decision_weights.append(dec_weight)
        else:
            dec_weight = pw.weigh_tversky_kahneman(
                sum(probs_sorted[: i + 1]), d
            ) - pw.weigh_tversky_kahneman(sum(probs_sorted[:i]), d)
            decision_weights.append(dec_weight)
    ind_vals = [
        pays_sorted_ut[i] * decision_weights[i] for i in range(len(pays_sorted_ut))
    ]
    return sum(ind_vals)


def cumulative_prospect_theory(
    pays, probs, d=0.65, a=0.88, l=2.25, util_function=um.utility_tversky_kahneman
):
    # TODO check against website
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
            dec_weight_pos = pw.weigh_tversky_kahneman(
                sum(probs_sorted_pos[: i + 1]), d
            )
            decision_weights_pos.append(dec_weight_pos)
        else:
            dec_weight_pos = pw.weigh_tversky_kahneman(
                sum(probs_sorted_pos[: i + 1]), d
            ) - pw.weigh_tversky_kahneman(sum(probs_sorted_pos[:i]), d)
            decision_weights_pos.append(dec_weight_pos)
    decision_weights_neg = []
    for i, _ in enumerate(probs_sorted_neg):
        if i == 0:
            dec_weight_neg = pw.weigh_tversky_kahneman(
                sum(probs_sorted_neg[: i + 1]), d
            )
            decision_weights_neg.append(dec_weight_neg)
        else:
            dec_weight_neg = pw.weigh_tversky_kahneman(
                sum(probs_sorted_neg[: i + 1]), d
            ) - pw.weigh_tversky_kahneman(sum(probs_sorted_neg[:i]), d)
            decision_weights_neg.append(dec_weight_neg)
    # collect all outcomes
    probs_final = decision_weights_pos + decision_weights_neg
    # modify utilites
    pays_final = [util_function(i) for i in pays_sorted_pos] + [
        util_function(i) for i in pays_sorted_neg
    ]
    ind_vals = [pays_final[i] * probs_final[i] for i in range(len(pays_final))]
    return sum(ind_vals)


# um.utility_tversky_kahneman(-3, r=0, a=0.88, l=2.25)
# um.root_utility(3)
# expected_utility([3, 2], [0.3, 0.7], util_function=um.lin_utility)
# rank_dependent_utility([1, 2], [0.4, 0.6], util_function=um.lin_utility)
# cumulative_prospect_theory([-3, 2], [0.4, 0.6])

