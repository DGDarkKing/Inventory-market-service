from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import ModelBaseUuid

if TYPE_CHECKING:
    from models.supplies import SupplyOrm
    from models.warehouse_goods import WarehouseGoodsOrm
    from models.trading_floor_goods import TradingFloorGoodsOrm


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
    warehouse_goods: Mapped["WarehouseGoodsOrm"] = relationship(
        back_populates="goods_meta",
    )
    trading_floor_goods: Mapped["TradingFloorGoodsOrm"] = relationship(
        back_populates="goods_meta",
    )
