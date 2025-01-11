from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field, AliasPath


class ExpirationGoodsMeta(BaseModel):
    id: UUID
    name: str = Field(
        validation_alias=AliasPath("goods_meta", "name"),
    )
    remains: float


class GoodsExpirationBase(BaseModel):
    id: UUID
    supply_id: UUID = Field(serialization_alias="supply")
    quantity: float
    remains: float
    expiration_time: datetime
    is_decommissioned: bool = Field(serialization_alias="isDecommissioned")


class GoodsExpiration(GoodsExpirationBase):
    pass


class GoodsExpirationFullData(GoodsExpirationBase):
    user_id: UUID = Field(serialization_alias="user")
    created_at: datetime
    updated_at: datetime
