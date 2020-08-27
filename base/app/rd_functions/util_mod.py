import sys
from simpleeval import simple_eval
import math

# TODO check https://en.wikipedia.org/wiki/Expected_utility_hypothesis for more interesing utility functions


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
        print("Please provide only positive payoffs when using this utility function")
        # TODO check if we need sys.exit(1)
    else:
        return x ** (1 / exp)


def lin_utility(x: float) -> float:
    """
    A linear utility function where the utility of a value x equals x
    """
    return x


def bern_utility(x: float) -> float:
    """ A simple utility function based on bernoulli's initial formulation of EU """
    if x <= 0:
        print("Please provide only positive payoffs when using this utility function")
        # TODO check if we need sys.exit(1)
    else:
        return math.log(x)


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

