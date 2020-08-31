import numpy as np
from simpleeval import simple_eval
import math

import rd_functions.custom_exceptions as ce


def weigh_tversky_kahneman(p: float, d: float = 0.65) -> float:
    """
    This returns the decision weight of a single input. The formula is based on Tversky and Kahneman and the classic value for d is 0.65
    """
    # TODO come up with a consisten way of testing inputs
    if p < 0 or p > 1:
        raise ce.ZeroToOneOnlyError
    elif d < 0:
        raise ce.NonNegativeValuesOnly
    else:
        return (p ** d) / ((p ** d + (1 - p) ** d) ** (1 / d))


def weigh_goldstein_einhorn(p: float, b: float = 0.5, a: float = 0.6) -> float:
    if p < 0 or p > 1:
        raise ce.ZeroToOneOnlyError
    elif b < 0:
        raise ce.PositiveValuesOnlyError
    else:
        return ((b * p) ** a) / ((b * p) ** a + (1 - p) ** a)


def weigh_prelec(p: float, b: float = 0.5, a: float = 0.6) -> float:
    if p < 0 or p > 1:
        print("p has to be between 0 and 1")
    else:
        return np.exp(-b * (-np.log(p)) ** a)


def weig_user(x: float, text: str) -> float:
    """ 
    Takes in a string and evaluates it (safely) with the simpleeval
    model to allow users to define their own probability weighting functions
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

