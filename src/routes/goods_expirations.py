from uuid import UUID

from fastapi import APIRouter

from auth.roles import Roles
from dependencies import RoleAccessDeps, WarehouseServiceDeps, UnitOfWorkDeps
from schemas.goods_expitration import GoodsExpirationFullData, GoodsExpiration
from schemas.goods_expitration_filters import GoodsExpirationFilter, GoodsExpiredFilter
from schemas.product_count import ProductCount

router = APIRouter(
    prefix="/goods/expirations",
    tags=["Warehouse"],
)


@router.get("/{id}", dependencies=[RoleAccessDeps(Roles.MANAGER, Roles.STOREKEEPER)])
async def get_goods_expiration(
    id: UUID,
    uow: UnitOfWorkDeps,
    warehouse_service: WarehouseServiceDeps,
) -> GoodsExpirationFullData | None:
    async with uow:
        result = await warehouse_service.get_goods(id)
        await uow.commit()
    return result


# get list by supply
# get list by expiration time
# get list by goods name
@router.get("", dependencies=[RoleAccessDeps(Roles.MANAGER, Roles.STOREKEEPER)])
async def get_goods_expiration_list(
    goods_expiration_filter: GoodsExpirationFilter,
    # paginator: Paginator,
    uow: UnitOfWorkDeps,
    warehouse_service: WarehouseServiceDeps,
) -> list[GoodsExpiration]:
    async with uow:
        result = await warehouse_service.get_goods_list(goods_expiration_filter)
        await uow.commit()
    return result


@router.get("/expired", dependencies=[RoleAccessDeps(Roles.MANAGER, Roles.STOREKEEPER)])
async def get_expired_goods(
    goods_expiration_filter: GoodsExpiredFilter,
    # paginator: Paginator,
    uow: UnitOfWorkDeps,
    warehouse_service: WarehouseServiceDeps,
) -> list[GoodsExpiration]:
    async with uow:
        result = await warehouse_service.get_expired_goods_list(goods_expiration_filter)
        await uow.commit()
    return result


@router.get("/count", dependencies=[RoleAccessDeps(Roles.MANAGER, Roles.STOREKEEPER)])
async def get_product_count(
    uow: UnitOfWorkDeps,
    warehouse_service: WarehouseServiceDeps,
) -> list[ProductCount]:
    async with uow:
        result = await warehouse_service.get_product_count()
        await uow.commit()
    return result


@router.post("")
async def create_goods_expiration(
    user: RoleAccessDeps(Roles.MANAGER, Roles.STOREKEEPER),
    goods_expiration: GoodsExpirationFullData,
    uow: UnitOfWorkDeps,
    warehouse_service: WarehouseServiceDeps,
) -> GoodsExpirationFullData:
    async with uow:
        result = await warehouse_service.accept_supply_goods(user.id, goods_expiration)
        await uow.commit()
    return result


@router.put("/{id}")
async def decommission_goods_expiration(
    id: UUID,
    user: RoleAccessDeps(Roles.MANAGER, Roles.STOREKEEPER),
    uow: UnitOfWorkDeps,
    warehouse_service: WarehouseServiceDeps,
) -> GoodsExpiration:
    async with uow:
        goods = await warehouse_service.decommission_goods(user.id, id)
        await uow.commit()
    return goods
