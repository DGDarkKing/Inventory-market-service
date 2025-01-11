from datetime import datetime
from uuid import UUID

from conditions.interfaces.base_specification import SqlAlchemySpecification
from models.trading_floor_deliveries import TradingFloorDeliveryOrm


class TradingFloorDeliveryById(SqlAlchemySpecification):
    def __init__(self, id: UUID):
        super().__init__(TradingFloorDeliveryOrm.id == id)


class TradingFloorDeliveryByGoodsName(SqlAlchemySpecification):
    def __init__(self, name: str):
        super().__init__(TradingFloorDeliveryOrm.goods.name.like(name))


class TradingFloorDeliveryByWarehouseGoodsId(SqlAlchemySpecification):
    def __init__(self, warehouse_goods_id: UUID):
        super().__init__(
            TradingFloorDeliveryOrm.goods_expiration_id == warehouse_goods_id
        )


class TradingFloorDeliveryByGoods(SqlAlchemySpecification):
    def __init__(self, goods_id: UUID):
        super().__init__(TradingFloorDeliveryOrm.goods_id == goods_id)


class TradingFloorDeliveryDecommissioned(SqlAlchemySpecification):
    def __init__(self, is_decommissioned: bool):
        super().__init__(TradingFloorDeliveryOrm.is_decommissioned == is_decommissioned)


class TradingFloorDeliveryMinRemains(SqlAlchemySpecification):
    def __init__(self, remains: float):
        super().__init__(TradingFloorDeliveryOrm.remains >= remains)


class TradingFloorDeliveryRemainsGreaterThan(SqlAlchemySpecification):
    def __init__(self, remains: float):
        super().__init__(TradingFloorDeliveryOrm.remains > remains)


class TradingFloorDeliveryExpirationFrom(SqlAlchemySpecification):
    def __init__(self, from_dt: datetime):
        super().__init__(TradingFloorDeliveryOrm.expiration_time >= from_dt)


class TradingFloorDeliveryExpirationTo(SqlAlchemySpecification):
    def __init__(self, to_dt: datetime):
        super().__init__(TradingFloorDeliveryOrm.expiration_time <= to_dt)


class TradingFloorDeliveryExpirationBetween(SqlAlchemySpecification):
    def __init__(self, from_dt: datetime | None, to_dt: datetime | None):
        if from_dt is not None and to_dt is not None:
            super().__init__(
                TradingFloorDeliveryOrm.expiration_time.between(from_dt, to_dt)
            )
        elif to_dt is None:
            super().__init__(TradingFloorDeliveryExpirationFrom(from_dt)._condition)
        elif from_dt is None:
            super().__init__(TradingFloorDeliveryExpirationTo(to_dt)._condition)
        else:
            raise ValueError("from_dt or to_dt must be is not None")
