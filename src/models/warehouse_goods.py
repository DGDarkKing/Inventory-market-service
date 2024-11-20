from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import ModelBaseUuid, ModelBase

if TYPE_CHECKING:
    from models.goods import GoodsOrm
    from models.goods_expirations import GoodsExpirationOrm


class WarehouseGoodsOrm(ModelBase):
    __tablename__ = "warehouse_goods"

    id: Mapped[UUID] = mapped_column(
        ForeignKey("goods.id"),
        unique=True,
    )
    remains: Mapped[float]

    goods_meta: Mapped["GoodsOrm"] = relationship(
        back_populates="warehouse_goods",
    )
    goods_expirations: Mapped[list["GoodsExpirationOrm"]] = relationship(
        back_populates="goods"
    )
