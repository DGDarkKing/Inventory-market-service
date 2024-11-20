from typing_extensions import Self

from orders.interfaces.i_order import IOrderSpecification


# INTEGRATION_TEST
class SaOrderSpecification(IOrderSpecification):
    def __init__(self, *orders):
        self.__orders = orders

    def complete(self) -> tuple:
        return self.__orders

    def __and__(self, other: "SaOrderSpecification") -> Self:
        return SaOrderSpecification(*self.__orders, *other.__orders)


def null_first_order(expression, flag: bool):
    if flag:
        return expression.nullsfirst()
    else:
        return expression.nullslast()
