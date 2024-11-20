from pathlib import Path

from pydantic import Field, BaseModel, ConfigDict, field_validator
from pydantic_core import Url
from pydantic_settings import BaseSettings


class AuthSettings(BaseModel):
    model_config = ConfigDict(validate_default=True)

    name: str = 'jwt'.upper()

    private_key: str = Field(description='Enter here key or path like string to read key from the file')
    public_key: str = Field(description='Enter here key or path like string to read key from the file')

    key_id: str = 'hypermarket-auth'
    key_type: str = 'RSA'
    algorithm: str = "RS256"

    audience: list[str]

    access_token_lifetime: int = Field(gt=0, default=3600)
    refresh_token_lifetime: int = Field(gt=0, default=24 * 60 * 60)

    @field_validator(
        'private_key',
        'public_key',
        mode='after'
    )
    @classmethod
    def _validate_keys(cls, data: str) -> str:
        path = Path(data)
        if path.exists():
            data = path.read_text()
        return data


class DatabaseSettings(BaseModel):
    host: str
    port: int = Field(gt=0)
    name: str
    user: str
    password: str
    max_connections: int = Field(gt=0, default=10)

    @property
    def db_async_url(self) -> str:
        return f'postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}'


class AppSettings(BaseSettings):
    my_url: Url
    name: str = "Hypermarket Warehouse Service"
    debug: bool = False
    secret_key: str = Field(min_length=10)
    oidc_discovery_url: str

    database: DatabaseSettings
    auth: AuthSettings


app_settings = AppSettings(
    _env_file=(
        f'{__file__}/../../envs/prod.env',
        f'{__file__}/../../envs/debug.env'
    ),
    _env_file_encoding='utf-8',
    _env_nested_delimiter='__'
)
