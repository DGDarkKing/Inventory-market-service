from sqlalchemy.sql.operators import and_, or_
from typing_extensions import Union, Self

from conditions.interfaces.i_specification import IConditionSpecification


class SqlAlchemySpecification(IConditionSpecification):
    def _get_not_empty_condtions(
        self, other
    ) -> (
        tuple["SqlAlchemySpecification"]
        | tuple["SqlAlchemySpecification", "SqlAlchemySpecification"]
    ):
        if self._condition is None and other._condition is not None:
            return (other,)
        if self._condition is not None and other._condition is None:
            return (self,)
        return (self, other)

    def __and__(self, other: IConditionSpecification) -> Self:
        not_empty = self._get_not_empty_condtions(other)
        if len(not_empty) == 1:
            return not_empty[0]
        return SqlAlchemySpecification((and_(self._condition, other._condition)))

    def __or__(self, other: IConditionSpecification) -> Self:
        not_empty = self._get_not_empty_condtions(other)
        if len(not_empty) == 1:
            return not_empty[0]
        return SqlAlchemySpecification((or_(self._condition, other._condition)))

    def __invert__(self) -> Self:
        if self._condition is None:
            return self
        return SqlAlchemySpecification(~self._condition)
