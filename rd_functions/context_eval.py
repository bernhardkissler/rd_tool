import rd_functions.util_mod as um
from simpleeval import simple_eval
import math
from functools import partial


def og_salience(x_1: float, x_2: float, theta: float = 0.1) -> float:
    # TODO check what theta is really supposed to do; Is it only supposed to prevent Div by zero? --> Doesn't say in the text. It is simply a degree of freedom to fit data
    """ basic salience function proposed as more tractable parametrization in original paper """
    return abs(x_1 - x_2) / (abs(x_1) + abs(x_2) + theta)


def user_salience(x_1: float, x_2: float, text: str = "") -> float:
    """Allow user to enter custom salience function

    Args:
        x_1 (float): primary payoff
        x_2 (float): context payoff
        text (str, optional): user entered function in one line to be evalued. Defaults to "".

    Returns:
        float: the salience of the compared values
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
        names={"x_1": x_1, "x_2": x_2},
    )

    return res


def ls_regret(
    x_1, x_2, um_function=um.lin_utility, um_kwargs={}, weight=1,
):
    """ classic regret function proposed by Loomes and Sugden 1982 """
    return um_function(x_1, **um_kwargs) + weight * (
        um_function(x_1, **um_kwargs) - um_function(x_2, **um_kwargs)
    )


def user_regret(
    x_1: float, x_2: float, um_function=um.lin_utility, um_kwargs={}, text: str = ""
) -> float:
    """ 
    Takes in a string and evaluates it (safely) with the simpleeval
    model to allow users to define their own regret functions
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
        names={"x_1": x_1, "x_2": x_2},
    )
    return res
