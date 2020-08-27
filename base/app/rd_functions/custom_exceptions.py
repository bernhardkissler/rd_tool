class PositiveValuesOnlyError(Exception):
    """ Is raised when function gets a value out of domain of funtion """

    pass


class ZeroToOneOnlyError(Exception):
    """ Is raised when a probability bigger than one or smaller than zero is fed to the function """

    pass


class NonNegativeValuesOnly(Exception):
    """ Is raised when a value which shouldn't be negative is supplied as negative """

    pass

