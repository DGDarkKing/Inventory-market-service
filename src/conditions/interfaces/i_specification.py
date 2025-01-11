from abc import ABC, abstractmethod

from typing_extensions import Self


class IConditionSpecification(ABC):
    def __init__(self, condition):
        self._condition = condition

    def complete(self):
        return self._condition

    @abstractmethod
    def __and__(self, other: "IConditionSpecification") -> Self:
        ...

    @abstractmethod
    def __or__(self, other: "IConditionSpecification") -> Self:
        ...

    @abstractmethod
    def __invert__(self) -> Self:
        ...
