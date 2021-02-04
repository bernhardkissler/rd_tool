import rd_functions.util_mod as um
from simpleeval import simple_eval
import math
from functools import partial


def additive_habits(
    c: float, y: float, um_function=um.lin_utility, um_kwargs={}, eta: float = 0.1
) -> float:
    """Bivariate utility function based on Muermann Gollier 2010 showing simple interaction dynamics

    Args:
        c (float): actual  payoff
        y (float): expected payoff 
        um_function (function): univariate utility function as used in EU
        eta (float): positive weight indicating the importance of expectations. Typicall 0 <eta<1

    Returns:
        float: utility of actual and expected payoff
    """
    return um_function(c - eta * y, **um_kwargs)


def additive_habits_ce(
    c: float,
    y: float,
    um_function=um.lin_utility,
    um_kwargs={},
    eta: float = 0.1,
    ce_function=um.lin_ce,
):
    """Inverse of additive habits utility function
    """
    return ce_function(c, **um_kwargs) + eta * y


def user_bivu(
    c: float, y: float, um_function=um.lin_utility, um_kwargs={}, text: str = ""
) -> float:
    """ 
    Takes in a string and evaluates it (safely) with the simpleeval
    model to allow users to define their own bivu functions
    """
    util_func = partial(um_function, **um_kwargs)

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
            "u": util_func,
        },
        names={"x_1": c, "x_2": y},
    )
    return res
