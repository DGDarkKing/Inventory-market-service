from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import ModelBaseUuid

if TYPE_CHECKING:
    from models.trading_floor_goods import TradingFloorGoodsAggregationOrm
    from models.goods_expirations import GoodsExpirationOrm


class TradingFloorDeliveryOrm(ModelBaseUuid):
    __tablename__ = "trading_floor_deliveries"

    user_id: Mapped[UUID]

    goods_expiration_id: Mapped[UUID] = mapped_column(
        ForeignKey("goods_expirations.id"),
    )
    goods_expiration: Mapped["GoodsExpirationOrm"] = relationship(
        back_populates="trading_floor_deliveries"
    )

    goods_id: Mapped[UUID] = mapped_column(
        ForeignKey("goods.id"),
    )
    goods: Mapped["TradingFloorGoodsAggregationOrm"] = relationship(
        back_populates="trading_floor_goods",
    )

    quantity: Mapped[float]
    remains: Mapped[float]

    expiration_time: Mapped[datetime]
    is_decommissioned: Mapped[bool] = mapped_column(
        default=False,
    )

    created_at: Mapped[datetime]
    updated_at: Mapped[datetime]
