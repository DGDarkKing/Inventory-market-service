from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import ModelBaseUuid

if TYPE_CHECKING:
    from models.warehouse_goods import WarehouseGoodsOrm
    from models.supplies import SupplyOrm
    from models.trading_floor_deliveries import TradingFloorDeliveryOrm


class GoodsExpirationOrm(ModelBaseUuid):
    __tablename__ = "goods_expirations"

    supply_id: Mapped[UUID] = mapped_column(
        ForeignKey("supplies.id"),
    )
    supply: Mapped["SupplyOrm"] = relationship(
        back_populates="goods_expirations",
    )

    goods_id: Mapped[UUID] = mapped_column(
        ForeignKey("warehouse_goods.id"),
    )
    goods: Mapped["WarehouseGoodsOrm"] = relationship(
        back_populates="goods_expirations",
    )

    quantity: Mapped[float]
    remains: Mapped[float]

    expiration_time: Mapped[datetime]
    is_decommissioned: Mapped[bool] = mapped_column(
        default=False,
    )

    created_at: Mapped[datetime]
    updated_at: Mapped[datetime]

    trading_floor_deliveries: Mapped[list["TradingFloorDeliveryOrm"]] = relationship(
        back_populates="goods_expiration"
    )
