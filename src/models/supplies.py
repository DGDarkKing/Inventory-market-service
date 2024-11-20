from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import ModelBaseUuid
from schemas.supply_states import SupplyState

if TYPE_CHECKING:
    from models.goods_expirations import GoodsExpirationOrm
    from models.goods import GoodsOrm


class SupplyOrm(ModelBaseUuid):
    __tablename__ = "supplies"

    quantity: Mapped[float]
    goods_id: Mapped[UUID] = mapped_column(
        ForeignKey("goods.id"),
    )
    goods: Mapped["GoodsOrm"] = relationship(
        back_populates="supplies",
    )

    manager_id: Mapped[UUID]
    storekeeper_id: Mapped[UUID]

    created_at: Mapped[datetime]
    updated_at: Mapped[datetime]

    goods_expirations: Mapped[list["GoodsExpirationOrm"]] = relationship(
        back_populates="supply"
    )
