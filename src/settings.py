from pathlib import Path

from pydantic import Field, BaseModel, ConfigDict, field_validator, UrlConstraints
from pydantic_core import Url
from pydantic_settings import BaseSettings
from typing_extensions import Annotated


class DatabaseSettings(BaseModel):
    host: str
    port: int = Field(gt=0)
    name: str
    user: str
    password: str
    max_connections: int = Field(gt=0, default=10)

    @property
    def db_async_url(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"


class AmqpSettings(BaseModel):
    url: Annotated[Url, UrlConstraints(allowed_schemes=["amqp"])]


class AppSettings(BaseSettings):
    my_url: Url
    name: str = "Hypermarket Inventory service"
    debug: bool = False
    oidc_discovery_url: str

    database: DatabaseSettings
    amqp: AmqpSettings


app_settings = AppSettings(
    _env_file=(f"{__file__}/../../envs/prod.env", f"{__file__}/../../envs/debug.env"),
    _env_file_encoding="utf-8",
    _env_nested_delimiter="__",
)
