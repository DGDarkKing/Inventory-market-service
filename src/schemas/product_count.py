from uuid import UUID

from pydantic import BaseModel


class ProductCount(BaseModel):
    id: UUID
    remains: float
