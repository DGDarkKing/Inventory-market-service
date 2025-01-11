from sqlalchemy.ext.asyncio import AsyncSession

from repositories.sa_repositories import (
    GoodsExpirationRepository,
    GoodsRepository,
    SupplyRepository,
    TradingFloorGoodsRepository,
    WarehouseGoodsRepository,
    OutboxRepository,
    TradingFloorDeliveryRepository,
)


class UnitOfWork:
    goods_repo: GoodsRepository
    goods_expiration_repo: GoodsExpirationRepository
    supply_repo: SupplyRepository
    trading_floor_delivery_repo: TradingFloorDeliveryRepository
    trading_floor_goods_aggregation_repo: TradingFloorGoodsRepository
    warehouse_goods_aggregation_repo: WarehouseGoodsRepository
    outbox_repo: OutboxRepository

    def __init__(self, session: AsyncSession):
        self.__session = session
        self.__session_counter = 0
        self.__current = 0
        self.__transactions = []

    def __init(self):
        if self.__session_counter == 1:
            self.goods_repo = GoodsRepository(self.__session)
            self.goods_expiration_repo = GoodsExpirationRepository(self.__session)
            self.supply_repo = SupplyRepository(self.__session)
            self.trading_floor_delivery_repo = TradingFloorDeliveryRepository(
                self.__session
            )
            self.trading_floor_goods_aggregation_repo = TradingFloorGoodsRepository(
                self.__session
            )
            self.warehouse_goods_aggregation_repo = WarehouseGoodsRepository(
                self.__session
            )
            self.outbox_repo = OutboxRepository(self.__session)

    async def __aenter__(self):
        self.__session_counter += 1
        self.__current += 1
        self.__init()

        if self.__session_counter == 2:
            self.__transactions.append(self.__session.begin())
        elif self.__session_counter > 2:
            self.__transactions.append(self.__session.begin_nested())

    def __del(self):
        if self.__session_counter == 0:
            del self.goods_repo
            del self.goods_expiration_repo
            del self.supply_repo
            del self.trading_floor_delivery_repo
            del self.trading_floor_goods_aggregation_repo
            del self.warehouse_goods_aggregation_repo
            del self.outbox_repo

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.rollback()
        if self.__session_counter - 1 == self.__current:
            self.__session_counter -= 1
            self.__del()

    async def commit(self):
        if self.__session_counter == self.__current:
            transaction = self.__get_transaction()
            await transaction.commit()
            self.__current -= 1

    async def rollback(self):
        if self.__session_counter == self.__current:
            transaction = self.__get_transaction()
            await transaction.rollback()
            self.__current -= 1

    async def flush(self):
        await self.__session.flush()

    def __get_transaction(self):
        return self.__transactions.pop() if self.__transactions else self.__session
