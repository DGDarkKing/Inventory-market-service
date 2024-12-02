import asyncio
import json
from abc import ABC, abstractmethod
from typing import TypeVar, Any

from faststream.broker.message import StreamMessage
from typing_extensions import Type, Generic, get_origin, get_args


class IMessageFilter(ABC):
    @abstractmethod
    async def __call__(self, message: StreamMessage) -> bool:
        ...


BodyType = TypeVar("BodyType")


class IBodyTypeFilter(IMessageFilter, Generic[BodyType]):
    target_type: Type[BodyType]

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        # Поиск оригинальной базы с generic-типами
        for base in cls.__orig_bases__:
            if get_origin(base) is IBodyTypeFilter:
                target_type = get_args(base)
                if target_type:
                    cls.target_type = target_type[0]
                    break

    def check_instance(self, body) -> bool:
        return isinstance(body, self.__class__.target_type)

    def _parse(self, message: StreamMessage) -> Any | None:
        try:
            body = json.loads(message.body)
            if self.check_instance(body):
                return body
        except Exception as ex:
            ...
        return None


class BodyTypeFilter(IBodyTypeFilter[BodyType]):
    def __init__(self, target_type: Type[BodyType]):
        self.target_type = target_type

    def check_instance(self, body) -> bool:
        return isinstance(body, self.target_type)

    async def __call__(self, message: StreamMessage) -> bool:
        return self._parse(message) is not None


class TypeInIBodyFilter(IBodyTypeFilter[dict]):
    def __init__(
        self,
        type_literal: str,
        type_arg_name: str = "type",
    ):
        super().__init__()
        self.type_arg_name = type_arg_name
        self.type_literal = type_literal

    async def __call__(self, message: StreamMessage) -> bool:
        if (body := self._parse(message)) is None:
            return False
        type = body.get(self.type_arg_name)
        return type is not None and type == self.type_literal
