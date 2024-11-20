from uuid import UUID

from pydantic import BaseModel


class UserModel(BaseModel):
    id: UUID
    first_name: str
    middle_name: str
    last_name: str
    role: str
