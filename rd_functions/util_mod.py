from math import nan
from rd_functions.custom_exceptions import PositiveValuesOnlyError

# import sys
from simpleeval import simple_eval
import math
import rd_functions.custom_exceptions as ce

# TODO check https://en.wikipedia.org/wiki/Expected_utility_hypothesis for more interesing utility functions
# https://en.wikipedia.org/wiki/Isoelastic_utility


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


def ce_tversky_kahneman(
    x: float, r: float = 0, a: float = 0.88, l: float = 2.25
) -> float:
    """ inverse of tk utility """
    if x >= r:
        outcome = x ** (1 / a) + r
    else:
        outcome = -((-x / l) ** (1 / a)) + r
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


def root_ce(x: float, exp: float = 2.0) -> float:
    """ inverse of root utility """
    return x ** exp


def lin_utility(x: float) -> float:
    """ A linear utility function; the utility of a value x equals x """
    return x


def lin_ce(x: float) -> float:
    """ Inverse of lin utility """
    return x


def bern_utility(x: float, a: float = 0) -> float:
    """ A simple utility function based on bernoulli's initial formulation of EU """
    try:
        res = math.log(a + x)
    except ValueError:
        res = nan
        raise ce.PositiveValuesOnlyError
    return res


def bern_ce(x: float, a: float = 0) -> float:
    """ Inverse of bernoulli utility """
    return math.exp(a + x)


# MARK Not utiltized in app
def pow_utility(x: float, exp: float = 2) -> float:
    """ Simple power utility function according to Stott 2006"""
    return x ** exp


# MARK Not utiltized in app
def quad_utility(x: float, a: float = 1) -> float:
    """ Simple quadratic utility function according to Stott 2006"""
    return a * x - x ** 2


def exp_utility(x: float, a: float = 1) -> float:
    """ Simple Exponential utility function according to Stott 2006"""
    return 1 - math.exp(-a * x)


def exp_ce(x: float, a: float = 1) -> float:
    """ Inverse of exp_utility """
    return -math.log(1 - x) / a


# MARK Not utiltized in app
def bell_utility(x: float, a: float = 1, b: float = 1) -> float:
    """ Simple Bell utility function according to Stott 2006"""
    return b * x - math.exp(-a * x)


# MARK Not utiltized in app
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


def user_ce(x: float, text: str) -> float:
    """ placeholder """
    return math.nan


# TODO find out how to solve user supplied functions for certainty equivalents with simpy !!! This will probably not work with piecewise definitions
