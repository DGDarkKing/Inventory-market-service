from fastapi import HTTPException
from starlette.status import HTTP_403_FORBIDDEN

from auth.user_model import UserModel


class RoleAccess:
    def __init__(self, *roles: str):
        self.__roles = roles
        if len(self.__roles) == 1:
            self.__roles = tuple(self.__roles[0].replace(" ", "").split(","))

    async def __call__(self, user: dict | UserModel) -> dict | UserModel:
        user_role: list[str] | str | None
        if isinstance(user, dict):
            user_role = user.get("role")
        else:
            user_role = getattr(user, "role", None)

        if user_role is None:
            raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Role not found")

        if isinstance(user_role, str):
            user_role = user_role.replace(" ", "").split(",")

        for role in self.__roles:
            if role in user_role:
                return user

        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Role forbidden")
