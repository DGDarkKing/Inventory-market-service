from datetime import datetime
from uuid import UUID

from conditions.interfaces.base_specification import SqlAlchemySpecification
from models.goods_expirations import GoodsExpirationOrm
from models.supplies import SupplyOrm
from models.warehouse_goods import WarehouseGoodsAggregationOrm


class WarehouseGoodsAggregationById(SqlAlchemySpecification):
    def __init__(self, id: UUID):
        super().__init__(WarehouseGoodsAggregationOrm.id == id)
