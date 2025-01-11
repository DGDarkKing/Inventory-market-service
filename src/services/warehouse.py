from datetime import datetime
from uuid import UUID

from pydantic import TypeAdapter

from conditions.expiration_goods import (
    GoodsExpirationById,
    GoodsExpirationDecommissioned,
    GoodsExpirationRemainsGreaterThan,
)
from conditions.supply import SupplyById
from conditions.warehouse_goods_aggregation import WarehouseGoodsAggregationById
from models.goods_expirations import GoodsExpirationOrm
from models.supplies import SupplyOrm
from models.warehouse_goods import WarehouseGoodsAggregationOrm
from schemas.goods_expitration import GoodsExpirationFullData, GoodsExpiration
from schemas.goods_expitration_filters import (
    GoodsExpirationFilter,
    GoodsExpiredFilter,
)
from schemas.product_count import ProductCount
from utils.unit_of_work import UnitOfWork


class WarehouseService:
    def __init__(
        self,
        uow: UnitOfWork,
    ):
        self.__uow = uow

    async def get_product_count(self) -> list[ProductCount]:
        aggregators: list[
            WarehouseGoodsAggregationOrm
        ] = await self.__uow.warehouse_goods_aggregation_repo.get_all()
        result = []
        if aggregators:
            adapter = TypeAdapter(list[ProductCount])
            result = adapter.validate_python(aggregators, from_attributes=True)
        return result

    async def get_goods(
        self,
        id: UUID,
    ) -> GoodsExpirationFullData | None:
        model = await self.__uow.goods_expiration_repo.get(
            GoodsExpirationById(id),
        )
        return (
            GoodsExpirationFullData.model_validate(model, from_attributes=True)
            if model
            else None
        )

    async def get_goods_list(
        self,
        goods_expiration_filter: GoodsExpirationFilter,
        # paginator: Paginator,
    ) -> list[GoodsExpiration]:
        model_list = await self.__uow.goods_expiration_repo.get_all(
            goods_expiration_filter.condition,
        )
        return TypeAdapter(
            list[GoodsExpiration],
        ).validate_python(model_list, from_attributes=True)

    async def get_expired_goods_list(
        self,
        goods_expiration_filter: GoodsExpiredFilter,
        # paginator: Paginator,
    ) -> list[GoodsExpiration]:
        model_list = await self.__uow.goods_expiration_repo.get_all(
            (
                goods_expiration_filter.condition
                & GoodsExpirationDecommissioned(False)
                & GoodsExpirationRemainsGreaterThan(0)
            ),
        )
        return TypeAdapter(
            list[GoodsExpiration],
        ).validate_python(model_list, from_attributes=True)

    async def accept_supply_goods(
        self,
        user_id: UUID,
        goods_expiration: GoodsExpirationFullData,
    ) -> GoodsExpirationFullData:
        if goods_expiration.expiration_time >= datetime.utcnow():
            raise ValueError(
                f"expiration time {goods_expiration.expiration_time.isoformat()} expired"
            )

        supply: SupplyOrm | None = await self.__uow.supply_repo.get(
            SupplyById(goods_expiration.supply_id)
        )
        if not supply:
            raise ValueError(f"supply {goods_expiration.supply_id} non-exists")

        aggregation: WarehouseGoodsAggregationOrm | None = await (
            self.__uow.warehouse_goods_aggregation_repo.get(
                WarehouseGoodsAggregationById(supply.goods_id)
            )
        )
        aggregation.remains += goods_expiration.quantity
        goods = GoodsExpirationOrm(
            user_id=user_id,
            supply_id=goods_expiration.supply_id,
            goods_id=supply.goods_id,
            quantity=goods_expiration.quantity,
            remains=goods_expiration.quantity,
            expiration_time=goods_expiration.expiration_time,
        )
        self.__uow.goods_expiration_repo.add([goods])
        return GoodsExpirationFullData.model_validate(goods, from_attributes=True)

    async def decommission_goods(
        self,
        user_id: UUID,
        id: UUID,
    ) -> GoodsExpiration:
        goods: GoodsExpirationOrm | None = await self.__uow.goods_expiration_repo.get(
            GoodsExpirationById(id)
        )
        if not goods:
            raise ValueError(f"goods expiration {id} non-exists")
        if goods.is_decommissioned:
            return GoodsExpiration.model_validate(goods, from_attributes=True)

        goods.user_id = user_id
        goods.is_decommissioned = True
        aggregation: WarehouseGoodsAggregationOrm | None = await (
            self.__uow.warehouse_goods_aggregation_repo.get(
                WarehouseGoodsAggregationById(goods.goods_id)
            )
        )
        aggregation -= goods.remains
        return GoodsExpiration.model_validate(goods, from_attributes=True)
