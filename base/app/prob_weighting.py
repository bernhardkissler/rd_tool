def weigh_tversky_kahneman(p: float, d: float = 0.65) -> float:
    """
    This returns the decision weight of a single input. The formula is based on Tversky and Kahneman and the classic value for d is 0.65
    """
    # TODO check checks
    if type(p) != float and type(p) != int:
        print("p must be a number")
    elif p < 0 or p > 1:
        print("p has to be between 0 and 1")
    elif type(d) != float and type(d) != int:
        print("d must be a number")
    else:
        return (p ** d) / ((p ** d + (1 - p) ** d) ** (1 / d))
