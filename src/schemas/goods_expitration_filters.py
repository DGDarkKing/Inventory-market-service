from datetime import datetime
from typing import Any
from typing_extensions import Self
from uuid import UUID

from pydantic import BaseModel, Field, model_validator

from conditions.empty import EmptyCondition
from conditions.expiration_goods import (
    GoodsExpirationByGoodsName,
    GoodsExpirationBySupply,
    GoodsExpirationByGoods,
    GoodsExpirationDecommissioned,
    GoodsExpirationMinRemains,
    GoodsExpirationExpirationBetween,
)
from conditions.interfaces.base_specification import SqlAlchemySpecification


class GoodsExpirationBaseFilter(BaseModel):
    goods_name: str | None = Field(
        validation_alias="name",
        default=None,
        min_length=1,
    )
    supply_id: UUID | None = Field(
        validation_alias="supply",
        default=None,
    )
    goods_id: UUID | None = Field(
        validation_alias="goods",
        default=None,
    )

    @model_validator(mode="after")
    def validate_supply_and_goods(self) -> Self:
        if self.supply_id is None and self.goods_id is None:
            raise ValueError("supply and goods can not be together")
        return self

    @model_validator(mode="after")
    def validate_name_and_goods(self) -> Self:
        if self.goods_name is None and self.goods_id is None:
            raise ValueError("name and goods can not be together")
        return self

    @property
    def empty(self):
        return (
            self.goods_name is None and self.supply_id is None and self.goods_id is None
        )

    @property
    def condition(self) -> SqlAlchemySpecification:
        condition = EmptyCondition()
        if self.empty:
            return condition

        if self.goods_name is not None:
            condition &= GoodsExpirationByGoodsName(self.goods_name)
        if self.supply_id is not None:
            condition &= GoodsExpirationBySupply(self.supply_id)
        if self.goods_id is not None:
            condition &= GoodsExpirationByGoods(self.goods_id)
        return condition


class GoodsExpiredFilter(GoodsExpirationBaseFilter):
    pass


class GoodsExpirationFilter(GoodsExpirationBaseFilter):
    is_decommissioned: bool | None = Field(
        validation_alias="decommissioned",
        default=True,
    )
    remains_from: int | None = Field(
        validation_alias="remains",
        default=None,
        ge=0,
    )
    expiration_time_from: datetime | None = Field(
        validation_alias="expiration_from",
        default=None,
    )
    expiration_time_to: datetime | None = Field(
        validation_alias="expiration_to",
        default=None,
    )

    @model_validator(mode="after")
    def validate_expiration_from_to(self) -> Self:
        if (
            self.expiration_time_from is not None
            and self.expiration_time_to is not None
            and (self.expiration_time_from > self.expiration_time_to)
        ):
            self.expiration_time_from, self.expiration_time_to = (
                self.expiration_time_to,
                self.expiration_time_from,
            )
        return self

    @property
    def expiration_range_exists(self) -> bool:
        return (
            self.expiration_time_from is not None or self.expiration_time_to is not None
        )

    @property
    def empty(self):
        return (
            super().empty
            and self.is_decommissioned is None
            and self.remains_from is None
            and self.expiration_time_from is None
            and self.expiration_time_to is None
        )

    @property
    def condition(self) -> SqlAlchemySpecification:
        condition = EmptyCondition()
        if self.empty:
            return condition

        condition = super().condition
        if self.is_decommissioned is not None:
            condition &= GoodsExpirationDecommissioned(self.is_decommissioned)
        if self.remains_from is not None:
            condition &= GoodsExpirationMinRemains(self.remains_from)
        if self.expiration_range_exists:
            condition &= GoodsExpirationExpirationBetween(
                self.expiration_time_from, self.expiration_time_to
            )
        return condition
