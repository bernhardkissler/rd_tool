from math import nan
from rd_functions.custom_exceptions import PositiveValuesOnlyError

# import sys
from simpleeval import simple_eval
import math
import rd_functions.custom_exceptions as ce

# TODO check https://en.wikipedia.org/wiki/Expected_utility_hypothesis for more interesing utility functions
# https://en.wikipedia.org/wiki/Utility#Examples


def utility_tversky_kahneman(
    x: float, r: float = 0, a: float = 0.88, l: float = 2.25
) -> float:
    """
    This is the classic tversky kahneman proposal for a utility function with common estimates of a = 0.88 and l = 2.25
    """
    if x >= r:
        outcome = (x - r) ** a
    else:
        outcome = -l * (-(x - r)) ** a
    return outcome


def root_utility(x: float, exp: float = 2.0) -> float:
    """
    A simple root utility function with u(x) = x**1/exp; by default the quadratic root is used
    """
    if x <= 0:
        res = nan
        raise ce.PositiveValuesOnlyError
    else:
        res = x ** (1 / exp)
    return res


def lin_utility(x: float) -> float:
    """ A linear utility function where the utility of a value x equals x """
    return x


def bern_utility(x: float, a: float = 0) -> float:
    """ A simple utility function based on bernoulli's initial formulation of EU """
    try:
        res = math.log(a + x)
    except ValueError:
        res = nan
        raise ce.PositiveValuesOnlyError
    return res


def pow_utility(x: float, exp: float = 2) -> float:
    """ Simple power utility function according to Stott 2006"""
    return x ** exp


def quad_utility(x: float, a: float = 1) -> float:
    """ Simple quadratic utility function according to Stott 2006"""
    return a * x - x ** 2


def exp_utility(x: float, a: float = 1) -> float:
    """ Simple Exponential utility function according to Stott 2006"""
    return 1 - math.exp(-a * x)


def bell_utility(x: float, a: float = 1, b: float = 1) -> float:
    """ Simple Bell utility function according to Stott 2006"""
    return b * x - math.exp(-a * x)


def hara_utility(x: float, a: float = 1, b: float = 1) -> float:
    """ Simple hara utility function according to Stott 2006"""
    return -((b + x) ** a)


def user_utility(x: float, text: str) -> float:
    """ 
    Takes in a string and evaluates it (safely) with the simpleeval
    model to allow users to define their own utility functions
    """
    res = simple_eval(
        text,
        functions={
            # "print": print,
            "abs": abs,
            "sin": math.sin,
            "cos": math.cos,
            "tan": math.tan,
            "e": math.e,
            "exp": math.exp,
            "log": math.log,
            "log10": math.log10,
            "pi": math.pi,
            "sqrt": math.sqrt,
        },
        names={"x": x},
    )
    return res

