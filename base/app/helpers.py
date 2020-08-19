import sys
from typing import List


def list_cleaning(pays: List[float], probs: List[float]):
    """
    makes sure that the two arguments are: list of numbers and have equal length; probs have to add to 1
    """
    if type(pays) != list or type(probs) != list:
        print("Please provide two lists of equal length as inputs")
        sys.exit(1)

    elif len(pays) != len(probs):
        print("Please provide two lists of equal length as inputs")
        sys.exit(1)
    else:
        try:
            pays_fl = [float(i) for i in pays]
            probs_fl = [float(i) for i in probs]
        except:
            print("Please provide two lists of numbers as inputs")
            sys.exit(1)
        # TODO research how to properly round things like [0.33,0.33,0.33] to 1
        if sum(probs_fl) != 1:
            print("Your list of probabilities has to add up to 1")
            print("The sum is currently {}.".format(sum(probs_fl)))
            sys.exit(1)
        else:
            return pays_fl, probs_fl
