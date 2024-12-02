from uuid import UUID

from fastapi import APIRouter


router = APIRouter(
    prefix="/consumer/goods",
    tags=["Consumer"],
)


@router.get("/{id}")
async def get_goods(
    id: UUID,
) -> GoodsFullData:
    # TODO
    pass


@router.get("")
async def get_goods(
    goods_expiration_filter: ConsumerGoodsFilter,
    paginator: Paginator,
) -> list[Goods]:
    # TODO
    pass
