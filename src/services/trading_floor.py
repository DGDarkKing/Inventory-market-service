from datetime import datetime
from uuid import UUID

from pydantic import TypeAdapter

from conditions.expiration_goods import GoodsExpirationById
from conditions.trading_floor_deliveries import (
    TradingFloorDeliveryById,
    TradingFloorDeliveryRemainsGreaterThan,
    TradingFloorDeliveryDecommissioned,
)
from conditions.trading_goods_aggregation import TradingGoodsAggregationById
from joins.expiration_goods import GoodsExpirationJoinGoods
from models.goods_expirations import GoodsExpirationOrm
from models.trading_floor_deliveries import TradingFloorDeliveryOrm
from models.trading_floor_goods import TradingFloorGoodsAggregationOrm
from schemas.product_count import ProductCount
from schemas.trading_goods import TradingGoodsFullData, TradingGoods
from schemas.trading_goods_filters import TradingGoodsFilter, TradingGoodsExpiredFilter
from utils.unit_of_work import UnitOfWork


class TradingFloorService:
    def __init__(
        self,
        uow: UnitOfWork,
    ):
        self.__uow = uow

    async def get_product_count(self) -> list[ProductCount]:
        aggregators: list[
            TradingFloorGoodsAggregationOrm
        ] = await self.__uow.trading_floor_goods_aggregation_repo.get_all()
        result = []
        if aggregators:
            adapter = TypeAdapter(list[ProductCount])
            result = adapter.validate_python(aggregators, from_attributes=True)
        return result

    async def get_goods(
        self,
        id: UUID,
    ) -> TradingGoodsFullData | None:
        model = await self.__uow.trading_floor_delivery_repo.get(
            TradingFloorDeliveryById(id),
        )
        return (
            TradingGoodsFullData.model_validate(model, from_attributes=True)
            if model
            else None
        )

    async def get_goods_list(
        self,
        goods_expiration_filter: TradingGoodsFilter,
        # paginator: Paginator,
    ) -> list[TradingGoods]:
        model_list = await self.__uow.goods_expiration_repo.get_all(
            goods_expiration_filter.condition,
        )
        return TypeAdapter(
            list[TradingGoods],
        ).validate_python(model_list, from_attributes=True)

    async def get_expired_goods_list(
        self,
        goods_expiration_filter: TradingGoodsExpiredFilter,
        # paginator: Paginator,
    ) -> list[TradingGoods]:
        model_list = await self.__uow.goods_expiration_repo.get_all(
            (
                goods_expiration_filter.condition
                & TradingFloorDeliveryDecommissioned(False)
                & TradingFloorDeliveryRemainsGreaterThan(0)
            ),
        )
        return TypeAdapter(
            list[TradingGoods],
        ).validate_python(model_list, from_attributes=True)

    async def delivery_from_warehouse(
        self,
        user_id: UUID,
        delivery_goods: TradingGoodsFullData,
    ) -> TradingGoodsFullData:
        expiration_goods: GoodsExpirationOrm | None = (
            await self.__uow.goods_expiration_repo.get(
                GoodsExpirationById(delivery_goods.goods_expiration_id),
                GoodsExpirationJoinGoods(),
            )
        )
        if not expiration_goods:
            raise ValueError(f"goods on warehouse {delivery_goods.id} non-exists")
        if expiration_goods.expiration_time >= datetime.utcnow():
            raise ValueError(
                f"expiration time {delivery_goods.expiration_time.isoformat()} expired"
            )
        if not expiration_goods.goods.is_ready_for_sale:
            raise ValueError(
                f"goods on warehouse {delivery_goods.id} is not ready for sale"
            )

        aggregation: TradingFloorGoodsAggregationOrm | None = await (
            self.__uow.trading_floor_goods_aggregation_repo.get(
                TradingGoodsAggregationById(expiration_goods.goods_id),
            )
        )
        aggregation.remains += delivery_goods.quantity
        goods = GoodsExpirationOrm(
            user_id=user_id,
            supply_id=delivery_goods.supply_id,
            goods_id=expiration_goods.goods_id,
            quantity=delivery_goods.quantity,
            remains=delivery_goods.quantity,
            expiration_time=delivery_goods.expiration_time,
        )
        self.__uow.trading_floor_delivery_repo.add([goods])
        return TradingGoodsFullData.model_validate(goods, from_attributes=True)

    async def decommission_goods(
        self,
        user_id: UUID,
        id: UUID,
    ) -> TradingGoods:
        goods: TradingFloorDeliveryOrm | None = (
            await self.__uow.trading_floor_delivery_repo.get(
                TradingFloorDeliveryById(id)
            )
        )
        if not goods:
            raise ValueError(f"trading goods {id} non-exists")
        if goods.is_decommissioned:
            return TradingGoods.model_validate(goods, from_attributes=True)

        goods.user_id = user_id
        goods.is_decommissioned = True
        aggregation: TradingFloorGoodsAggregationOrm | None = await (
            self.__uow.trading_floor_goods_aggregation_repo.get(
                TradingGoodsAggregationById(goods.goods_id)
            )
        )
        aggregation -= goods.remains
        return TradingGoods.model_validate(goods, from_attributes=True)
