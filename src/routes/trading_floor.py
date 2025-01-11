from uuid import UUID

from fastapi import APIRouter

from auth.roles import Roles
from dependencies import RoleAccessDeps

router = APIRouter(
    prefix="/trading/floor/deliveries",
    tags=["Trading floor"],
)

#
# @router.get("/hello")
# async def hello(
#     user: RoleAccessDeps(Roles.MANAGER),
# ):
#     return user


#
# get one
@router.get("/{id}")
async def get_goods(
    id: UUID,
    user: RoleAccessDeps(Roles.MANAGER, Roles.CASHIER),
) -> TradingGoodsFullData:
    # TODO
    pass


# get list by expiration warehouse
# get list by expiration time
# get list by goods name
@router.get("")
async def get_goods_expiration(
    user: RoleAccessDeps(Roles.MANAGER, Roles.CASHIER),
    goods_expiration_filter: TradingGoodsFilter,
    # paginator: Paginator,
) -> list[TradingGoods]:
    # TODO
    pass


# get expired
@router.get("/expired")
async def get_goods_expired(
    user: RoleAccessDeps(Roles.MANAGER, Roles.CASHIER),
    goods_expiration_filter: TradingGoodsExpiredFilter,
    paginator: Paginator,
) -> list[TradingGoods]:
    # TODO
    pass


@router.get("/count", dependencies=[RoleAccessDeps(Roles.MANAGER, Roles.STOREKEEPER)])
async def get_product_count(
    uow: UnitOfWorkDeps,
    warehouse_service: WarehouseServiceDeps,
) -> list[ProductCount]:
    async with uow:
        result = dsadsadsadasd.get_product_count()
        await uow.commit()
    return result


# decommission
@router.put("/{id}")
async def decommission_goods(
    user: RoleAccessDeps(Roles.MANAGER, Roles.CASHIER),
    id: UUID,
):
    # TODO
    pass
