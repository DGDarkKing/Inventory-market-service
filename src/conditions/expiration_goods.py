from datetime import datetime
from uuid import UUID

from conditions.interfaces.base_specification import SqlAlchemySpecification
from models.goods_expirations import GoodsExpirationOrm


class GoodsExpirationById(SqlAlchemySpecification):
    def __init__(self, id: UUID):
        super().__init__(GoodsExpirationOrm.id == id)


class GoodsExpirationByGoodsName(SqlAlchemySpecification):
    def __init__(self, name: str):
        super().__init__(GoodsExpirationOrm.goods.goods_meta.name.like(name))


class GoodsExpirationBySupply(SqlAlchemySpecification):
    def __init__(self, supply_id: UUID):
        super().__init__(GoodsExpirationOrm.supply_id == supply_id)


class GoodsExpirationByGoods(SqlAlchemySpecification):
    def __init__(self, goods_id: UUID):
        super().__init__(GoodsExpirationOrm.goods_id == goods_id)


class GoodsExpirationDecommissioned(SqlAlchemySpecification):
    def __init__(self, is_decommissioned: bool):
        super().__init__(GoodsExpirationOrm.is_decommissioned == is_decommissioned)


class GoodsExpirationMinRemains(SqlAlchemySpecification):
    def __init__(self, remains: float):
        super().__init__(GoodsExpirationOrm.remains >= remains)


class GoodsExpirationRemainsGreaterThan(SqlAlchemySpecification):
    def __init__(self, remains: float):
        super().__init__(GoodsExpirationOrm.remains > remains)


class GoodsExpirationExpirationFrom(SqlAlchemySpecification):
    def __init__(self, from_dt: datetime):
        super().__init__(GoodsExpirationOrm.expiration_time >= from_dt)


class GoodsExpirationExpirationTo(SqlAlchemySpecification):
    def __init__(self, to_dt: datetime):
        super().__init__(GoodsExpirationOrm.expiration_time <= to_dt)


class GoodsExpirationExpirationBetween(SqlAlchemySpecification):
    def __init__(self, from_dt: datetime | None, to_dt: datetime | None):
        if from_dt is not None and to_dt is not None:
            super().__init__(GoodsExpirationOrm.expiration_time.between(from_dt, to_dt))
        elif to_dt is None:
            super().__init__(GoodsExpirationExpirationFrom(from_dt)._condition)
        elif from_dt is None:
            super().__init__(GoodsExpirationExpirationTo(to_dt)._condition)
        else:
            raise ValueError("from_dt or to_dt must be is not None")
