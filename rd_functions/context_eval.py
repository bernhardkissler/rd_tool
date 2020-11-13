import rd_functions.util_mod as um
from simpleeval import simple_eval
import math
from functools import partial


def ls_regret(
    x_1, x_2, weight, um_function, um_kwargs={},
):
    """ classic regret function proposed by Loomes and Sugden 1982 """
    return um_function(x_1, **um_kwargs) + weight * (
        um_function(x_1, **um_kwargs) - um_function(x_2, **um_kwargs)
    )


def user_regret(x: float, text: str, um_function=um.lin_utility, um_kwargs={}) -> float:
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
        names={"x": x},
    )
    return res
