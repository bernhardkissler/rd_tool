import sys


def utility_tversky_kahneman(x, r=0, a=0.88, l=2.25):
    """
    This is the classic tversky kahneman proposal for a utility function with common estimates of a = 0.88 and l = 2.25
    """
    if x >= r:
        outcome = (x - r) ** a
    else:
        outcome = -l * (-(x - r)) ** a
    return outcome


def root_utility(x, exp=2):
    """
    A simple root utility function with u(x) = x**1/exp; by default the quadratic root is used
    """
    if x < 0:
        print("Please provide only positive payoffs when using a root utility function")
        sys.exit(1)
    else:
        return x ** (1 / exp)


def lin_utility(x):
    """
    A linear utility function where the utility of a value x equals x
    """
    return x