from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import ModelBaseUuid

if TYPE_CHECKING:
    from models.supplies import SupplyOrm
    from models.goods_expirations import GoodsExpirationOrm
    from models.warehouse_goods import WarehouseGoodsAggregationOrm
    from models.trading_floor_deliveries import TradingFloorDeliveryOrm
    from models.trading_floor_goods import TradingFloorGoodsAggregationOrm


class GoodsOrm(ModelBaseUuid):
    __tablename__ = "goods"

    name: Mapped[str] = mapped_column(
        String(length=300),
        unique=True,
    )
    is_weighted: Mapped[bool]
    is_qrable: Mapped[bool]
    unique_code: Mapped[str] = mapped_column(
        String(length=50),
        unique=True,
    )

    created_at: Mapped[datetime]
    updated_at: Mapped[datetime]

    supplies: Mapped[list["SupplyOrm"]] = relationship(
        back_populates="goods",
    )
    warehouse_goods: Mapped["GoodsExpirationOrm"] = relationship(
        back_populates="goods",
    )
    warehouse_aggregated_goods: Mapped["WarehouseGoodsAggregationOrm"] = relationship(
        back_populates="goods",
    )
    trading_floor_goods: Mapped["TradingFloorDeliveryOrm"] = relationship(
        back_populates="goods",
    )
    trading_floor_aggregated_goods: Mapped[
        "TradingFloorGoodsAggregationOrm"
    ] = relationship(
        back_populates="goods",
    )
