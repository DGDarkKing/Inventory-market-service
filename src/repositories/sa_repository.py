from typing import Sequence

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from conditions.interfaces.i_specification import IConditionSpecification
from database import ModelBase
from joins.interfaces.i_join_specification import IJoinSpecification
from orders.interfaces.i_order import IOrderSpecification
from repositories.interfaces.i_repository import IRepository


class SaAsyncRepository(IRepository):
    _MODEL: ModelBase

    def __init__(self, session: AsyncSession):
        self._session = session

    def add(self, objs: list[ModelBase]):
        self._session.add_all(objs)

    async def delete(self, objs: list[ModelBase]):
        ids = [obj.id for obj in objs]
        stmt = delete(self._MODEL).where(self._MODEL.id.in_(ids))
        await self._session.execute(stmt)

    async def delete_by_condition(self, condition: IConditionSpecification = None):
        stmt = delete(self._MODEL)
        if condition:
            stmt = stmt.where(condition.complete())
        await self._session.execute(stmt)

    async def get_all(
            self,
            condition: IConditionSpecification = None,
            join: IJoinSpecification = None,
            order: IOrderSpecification = None,
            limit: int = 0
    ) -> Sequence[ModelBase]:
        query = select(self._MODEL)
        if condition:
            query = query.where(condition.complete())
        if join:
            query = query.options(*join.complete())
        if order:
            query = query.order_by(*order.complete())
        if limit > 0:
            query = query.limit(limit)

        res = await self._session.execute(query)
        return res.scalars().all()

    async def get(
            self,
            condition: IConditionSpecification = None,
            join: IJoinSpecification = None,
            order: IOrderSpecification = None,
    ) -> ModelBase | None:
        res = await self.get_all(condition, join, order, limit=1)
        return res[0] if res else None
