from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from auth.open_id_connect import create_openid_connect
from auth.role_based_access import RoleAccess
from auth.user_model import UserModel
from database import async_session_maker
from services import WarehouseService
from settings import app_settings
from utils.unit_of_work import UnitOfWork

TARGET_SESSION_MAKER = async_session_maker


async def create_unit_of_work(
    session: AsyncSession,
) -> UnitOfWork:
    return UnitOfWork(session)


UnitOfWorkDeps = Annotated[UnitOfWork, Depends(create_unit_of_work)]


OIDC = create_openid_connect(
    issuer="Hypermarket Authorization Server",
    audience="warehouse",
    strategy=HTTPBearer(),
    open_id_connect_url=app_settings.oidc_discovery_url,
)

UserDeps = Annotated[dict | UserModel, Depends(OIDC)]


def RoleAccessDeps(*roles: str):
    role_accessor = RoleAccess(*roles)

    async def wrapped(user: UserDeps):
        return await role_accessor(user)

    return Annotated[dict | UserModel, Depends(wrapped)]


def create_warehouse_service(
    uow: UnitOfWorkDeps,
) -> WarehouseService:
    return WarehouseService(uow)


WarehouseServiceDeps = Annotated[WarehouseService, Depends(create_warehouse_service)]
