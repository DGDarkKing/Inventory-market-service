from fastapi import APIRouter

from auth.roles import Roles
from dependencies import RoleAccessDeps

router = APIRouter(prefix="/supply")


@router.get("/hello")
async def hello(
    user: RoleAccessDeps(Roles.MANAGER),
):
    return user
