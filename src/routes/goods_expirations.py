from uuid import UUID

from fastapi import APIRouter

from auth.roles import Roles
from dependencies import RoleAccessDeps

router = APIRouter(
    prefix="/goods/expirations",
    tags=["Warehouse"],
)


# @router.get("/hello")
# async def hello(
#     user: RoleAccessDeps(Roles.MANAGER),
# ):
#     return user


#
# get one
@router.get("/{id}")
async def get_goods_expiration(
    id: UUID,
    user: RoleAccessDeps(Roles.MANAGER, Roles.STOREKEEPER),
) -> GoodsExpirationFullData:
    # TODO
    pass


# get list by supply
# get list by expiration time
# get list by goods name
@router.get("")
async def get_goods_expiration(
    user: RoleAccessDeps(Roles.MANAGER, Roles.STOREKEEPER),
    goods_expiration_filter: GoodsExpirationFilter,
    paginator: Paginator,
) -> list[GoodsExpiration]:
    # TODO
    pass


# get expired
@router.get("/expired")
async def get_goods_expirations(
    user: RoleAccessDeps(Roles.MANAGER, Roles.STOREKEEPER),
    goods_expiration_filter: GoodsExpiredFilter,
    paginator: Paginator,
) -> list[GoodsExpiration]:
    # TODO
    pass


#
# add_from_supply
@router.post("")
async def create_goods_expiration(
    user: RoleAccessDeps(Roles.MANAGER, Roles.STOREKEEPER),
    goods_expiration: GoodsExpirationFullData,
) -> GoodsExpirationFullData:
    # TODO
    pass


# decommission
@router.put("/{id}")
async def decommission_goods_expiration(
    user: RoleAccessDeps(Roles.MANAGER, Roles.STOREKEEPER),
    id: UUID,
):
    # TODO
    pass
