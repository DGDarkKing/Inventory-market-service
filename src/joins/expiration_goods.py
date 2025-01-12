from sqlalchemy.orm import joinedload, selectinload

from joins.sa_join import SaJoinSpecification
from models.goods_expirations import GoodsExpirationOrm
from models.warehouse_goods import WarehouseGoodsAggregationOrm


class GoodsExpirationJoinGoods(SaJoinSpecification):
    def __init__(self):
        super().__init__(joinedload(GoodsExpirationOrm.goods))
