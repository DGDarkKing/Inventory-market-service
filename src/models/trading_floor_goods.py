from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import ModelBaseUuid, ModelBase

if TYPE_CHECKING:
    from models.goods import GoodsOrm
    from models.goods_expirations import GoodsExpirationOrm


class TradingFloorGoodsOrm(ModelBase):
    __tablename__ = "trading_floor_goods"

    id: Mapped[UUID] = mapped_column(
        ForeignKey("goods.id"),
        unique=True,
    )
    remains: Mapped[float]

    goods_meta: Mapped["GoodsOrm"] = relationship(
        back_populates="trading_floor_goods",
    )
    trading_floor_deliveries: Mapped[list["GoodsExpirationOrm"]] = relationship(
        back_populates="goods"
    )
