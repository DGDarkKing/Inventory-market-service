from uuid import UUID

from conditions.interfaces.base_specification import SqlAlchemySpecification
from models.trading_floor_goods import TradingFloorGoodsAggregationOrm


class TradingGoodsAggregationById(SqlAlchemySpecification):
    def __init__(self, id: UUID):
        super().__init__(TradingFloorGoodsAggregationOrm.id == id)
