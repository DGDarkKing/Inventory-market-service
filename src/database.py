from datetime import datetime
from enum import Enum
from typing import Any
from uuid import UUID

from sqlalchemy import text, JSON
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import mapped_column, DeclarativeBase, Mapped
from typing_extensions import Annotated, AsyncGenerator

from settings import app_settings

async_engine = create_async_engine(
    app_settings.database.db_async_url,
    pool_size=app_settings.database.max_connections,
    echo=app_settings.debug,
)

async_session_maker = async_sessionmaker(
    async_engine,
    expire_on_commit=False,
)

IntPk = Annotated[int, mapped_column(primary_key=True)]
UuidPk = Annotated[UUID, mapped_column(primary_key=True)]
DateTimeNow = Annotated[
    datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))
]


class ModelBase(DeclarativeBase):
    type_annotation_map = {
        dict[str, Any]: JSON,
        list[Any]: JSON,
    }


class ModelBaseInt(ModelBase):
    __abstract__ = True
    id: Mapped[IntPk]


class ModelBaseUuid(ModelBase):
    __abstract__ = True
    id: Mapped[UuidPk]


def create_tables():
    ModelBase.metadata.create_all(async_engine.engine)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
