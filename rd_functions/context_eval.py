def ls_regret(
    x_1, x_2, weight, um_function, um_kwargs={},
):
    """ classic regret function proposed by Loomes and Sugden 1982 """
    return um_function(x_1, **um_kwargs) + weight * (
        um_function(x_1, **um_kwargs) - um_function(x_2, **um_kwargs)
    )
