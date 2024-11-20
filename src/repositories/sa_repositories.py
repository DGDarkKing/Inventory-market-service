from models.goods import GoodsOrm
from models.goods_expirations import GoodsExpirationOrm
from models.outbox import OutboxOrm
from models.supplies import SupplyOrm
from models.trading_floor_deliveries import TradingFloorDeliveryOrm
from models.trading_floor_goods import TradingFloorGoodsOrm
from models.warehouse_goods import WarehouseGoodsOrm
from repositories.sa_repository import SaAsyncRepository


class GoodsRepository(SaAsyncRepository):
    _MODEL = GoodsOrm


class GoodsExpirationRepository(SaAsyncRepository):
    _MODEL = GoodsExpirationOrm


class SupplyRepository(SaAsyncRepository):
    _MODEL = SupplyOrm


class TradingFloorDeliveryRepository(SaAsyncRepository):
    _MODEL = TradingFloorDeliveryOrm


class TradingFloorGoodsRepository(SaAsyncRepository):
    _MODEL = TradingFloorGoodsOrm


class WarehouseGoodsRepository(SaAsyncRepository):
    _MODEL = WarehouseGoodsOrm


class OutboxRepository(SaAsyncRepository):
    _MODEL = OutboxOrm