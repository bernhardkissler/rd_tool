from math import nan


def mean(pays, probs=None):
    try:
        res = sum([pays[i] * probs[i] for i in range(len(pays))])
    except:
        res = nan
    return res


# TODO add function for Median?


def std_dev(pays, probs):
    try:
        mean_helper = mean(pays, probs)
        res = sum(
            [(pays[i] - mean_helper) ** 2 * probs[i] for i in range(len(pays))]
        ) ** (1 / 2)
    except:
        res = nan
    return res


def skew(pays, probs):
    try:
        mean_helper = mean(pays, probs)
        std_dev_helper = std_dev(pays, probs)
        res = (
            sum([(pays[i] - mean_helper) ** 3 * probs[i] for i in range(len(pays))])
            / std_dev_helper ** 3
        )
    except:
        res = nan
    return res


def kurtosis(pays, probs):
    # Implements Excess kurtosis!!!!
    # TODO maybe implement an "excess kurtosis" formula i.e. kurtosis - 3 see https://www.macroption.com/kurtosis-formula/
    try:
        mean_helper = mean(pays, probs)
        std_dev_helper = std_dev(pays, probs)
        res = (
            sum([(pays[i] - mean_helper) ** 4 * probs[i] for i in range(len(pays))])
            / std_dev_helper ** 4
        ) - 3
    except:
        res = nan
    return res


# TODO add measures of financial risk from https://en.wikipedia.org/wiki/Risk_measure
# https://en.wikipedia.org/wiki/List_of_financial_performance_measures
# https://en.wikipedia.org/wiki/Risk_measure
# TODO add things like sharpe ratio?


# pays_test = [2, 4, 5, 7, 8, 10, 11, 25, 26, 27, 36]
# probs_test = [1 / len(pays_test) for _ in pays_test]

# pays_test_02 = [61, 64, 67, 70, 73]
# probs_test_02 = [i / sum([5, 18, 42, 27, 8]) for i in [5, 18, 42, 27, 8]]

# print(mean(pays_test_02, probs_test_02))
# print(std_dev(pays_test_02, probs_test_02))
# print(skew(pays_test_02, probs_test_02))
# print(kurtosis(pays_test_02, probs_test_02))
