import asyncio
from abc import abstractmethod, ABC
from typing import Type

import httpx
from fastapi import HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, OAuth2AuthorizationCodeBearer
from fastapi.security.api_key import APIKeyHeader, APIKeyCookie, APIKeyBase
from fastapi.security.base import SecurityBase
from fastapi.security.http import HTTPBase
from jose import jwt, JWTError
from starlette.requests import Request
from starlette.status import HTTP_403_FORBIDDEN
from typing_extensions import Doc, Annotated, Optional

from auth.open_id_connect_error import InvalidStrategy


class OpenIdConnectBase(SecurityBase, ABC):
    def __init__(
            self,
            *,
            issuer: str,
            audience: str,
            strategy: SecurityBase,
            open_id_connect_url: Annotated[
                str,
                Doc(
                    """
                The OpenID Connect URL.
                """
                ),
            ],
    ):
        self.strategy: SecurityBase = strategy
        self.model = self.strategy.model
        self.scheme_name = self.strategy.scheme_name

        self.audience = audience
        self.issuer = issuer
        self.open_id_connect_url = open_id_connect_url
        self.__public_keys: str = None
        self.__public_key_lock: asyncio.Lock = asyncio.Lock()

    @property
    def public_keys(self) -> str | None:
        return self.__public_keys

    async def __get_public_keys(self):
        if self.__public_keys is None:
            async with self.__public_key_lock:
                if self.__public_keys is None:
                    async with httpx.AsyncClient() as client:
                        response = await client.get(self.open_id_connect_url)
                        jwks_response = await client.get(response.json()['jwks_uri'])
                        self.__public_keys = jwks_response.json()

    @abstractmethod
    async def _handle(self, request: Request) -> Optional[str]:
        ...

    async def __call__(self, request: Request) -> Optional[dict]:
        await self.__get_public_keys()

        token = await self._handle(request)
        if token is None:
            return None

        try:
            payload = jwt.decode(
                token,
                key=self.__public_keys,
                issuer=self.issuer,
                audience=self.audience,
            )
            return payload
        except JWTError as ex:
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN, detail="Not authenticated"
            )


class OpenIdConnectApiKey(OpenIdConnectBase):
    strategy: APIKeyHeader

    async def _handle(self, request: Request) -> Optional[str]:
        return await self.strategy(request)


class OpenIdConnectCredentials(OpenIdConnectBase):
    strategy: HTTPBase

    async def _handle(self, request: Request) -> Optional[str]:
        credentials = await self.strategy.__call__(request)
        return credentials.credentials


def create_openid_connect(
        *,
        issuer: str,
        audience: str,
        strategy: SecurityBase,
        open_id_connect_url: Annotated[
            str,
            Doc(
                """
            The OpenID Connect URL.
            """
            ),
        ],
) -> OpenIdConnectBase:
    handlers: dict[Type[SecurityBase], Type[OpenIdConnectBase]] = {
        HTTPBearer: OpenIdConnectCredentials,
        APIKeyHeader: OpenIdConnectApiKey,
        APIKeyCookie: OpenIdConnectApiKey,
        OAuth2AuthorizationCodeBearer: OpenIdConnectApiKey,
    }
    handler = handlers.get(strategy.__class__)
    if not handlers:
        raise InvalidStrategy(
            f'Invalid strategy "{strategy.__class__}"',
            'Valid strategies: "HTTPBearer", "APIKeyHeader", "APIKeyCookie", "OAuth2AuthorizationCodeBearer"'
        )
    return handler(issuer=issuer, audience=audience, strategy=strategy, open_id_connect_url=open_id_connect_url)
