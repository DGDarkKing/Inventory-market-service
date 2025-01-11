from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field, AliasPath


class TradingGoodsBase(BaseModel):
    id: UUID
    goods_expiration_id: UUID = Field(serialization_alias="goods_expiration")
    goods_id: UUID = Field(serialization_alias="goods")
    quantity: float
    remains: float
    expiration_time: datetime
    is_decommissioned: bool = Field(serialization_alias="isDecommissioned")


class TradingGoods(TradingGoodsBase):
    pass


class TradingGoodsFullData(TradingGoodsBase):
    user_id: UUID = Field(serialization_alias="user")
    created_at: datetime
    updated_at: datetime
