from uuid import UUID

from fastapi import APIRouter

from auth.roles import Roles
from dependencies import RoleAccessDeps, TradingFloorServiceDeps, UnitOfWorkDeps
from schemas.product_count import ProductCount
from schemas.trading_goods import TradingGoodsFullData, TradingGoods
from schemas.trading_goods_filters import TradingGoodsExpiredFilter, TradingGoodsFilter

router = APIRouter(
    prefix="/trading/floor/deliveries",
    tags=["Trading floor"],
)


#
# get one
@router.get("/{id}", dependencies=[RoleAccessDeps(Roles.MANAGER, Roles.CASHIER)])
async def get_goods(
    id: UUID,
    user: RoleAccessDeps(Roles.MANAGER, Roles.CASHIER),
    uow: UnitOfWorkDeps,
    trading_floor_service: TradingFloorServiceDeps,
) -> TradingGoodsFullData | None:
    async with uow:
        result = await trading_floor_service.get_goods(id)
        await uow.commit()
    return result


# get list by expiration time
# get list by goods name
@router.get("", dependencies=[RoleAccessDeps(Roles.MANAGER, Roles.CASHIER)])
async def get_goods_expiration(
    uow: UnitOfWorkDeps,
    goods_expiration_filter: TradingGoodsFilter,
    trading_floor_service: TradingFloorServiceDeps,
    # paginator: Paginator,
) -> list[TradingGoods]:
    async with uow:
        result = await trading_floor_service.get_goods_list(goods_expiration_filter)
        await uow.commit()
    return result


# get expired
@router.get("/expired", dependencies=[RoleAccessDeps(Roles.MANAGER, Roles.CASHIER)])
async def get_goods_expired(
    uow: UnitOfWorkDeps,
    goods_expiration_filter: TradingGoodsExpiredFilter,
    trading_floor_service: TradingFloorServiceDeps,
    # paginator: Paginator,
) -> list[TradingGoods]:
    async with uow:
        result = await trading_floor_service.get_expired_goods_list(
            goods_expiration_filter
        )
        await uow.commit()
    return result


@router.get("/count", dependencies=[RoleAccessDeps(Roles.MANAGER, Roles.STOREKEEPER)])
async def get_product_count(
    uow: UnitOfWorkDeps,
    trading_floor_service: TradingFloorServiceDeps,
) -> list[ProductCount]:
    async with uow:
        result = await trading_floor_service.get_product_count()
        await uow.commit()
    return result


@router.put("/deliver")
async def deliver_from_warehouse(
    user: RoleAccessDeps(Roles.MANAGER, Roles.CASHIER),
    goods: TradingGoodsFullData,
    uow: UnitOfWorkDeps,
    trading_floor_service: TradingFloorServiceDeps,
) -> TradingGoodsFullData:
    async with uow:
        result = await trading_floor_service.delivery_from_warehouse(goods)
        await uow.commit()
    return result


# decommission
@router.put("/{id}")
async def decommission_goods(
    user: RoleAccessDeps(Roles.MANAGER, Roles.CASHIER),
    id: UUID,
    uow: UnitOfWorkDeps,
    trading_floor_service: TradingFloorServiceDeps,
) -> TradingGoods:
    async with uow:
        result = await trading_floor_service.decommission_goods(id)
        await uow.commit()
    return result
