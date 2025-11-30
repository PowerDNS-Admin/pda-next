from datetime import timedelta, datetime
from typing import Dict, Optional

from fastapi import Request
from fastapi.openapi.models import OAuthFlowClientCredentials
from fastapi.security import OAuth2, HTTPBasic
from fastapi.security.oauth2 import OAuthFlowsModel
from jose import jwt

from lib.permissions import Permissions
from lib.security import ACCESS_TOKEN_AGE, ALGORITHM


class ClientCredentialsBearer(OAuth2):
    """Provides a custom OAuth2 scheme for using just client credentials."""
    def __init__(
            self,
            tokenUrl: str,
            refreshUrl: Optional[str] = None,
            scopes: Dict[str, str] = None,
            scheme_name: Optional[str] = None,
            auto_error: bool = True,
    ):
        flows = OAuthFlowsModel(
            clientCredentials=OAuthFlowClientCredentials(
                tokenUrl=tokenUrl,
                refreshUrl=refreshUrl,
                scopes=scopes or {},
            ),
        )
        super().__init__(flows=flows, scheme_name=scheme_name, auto_error=auto_error)

    async def __call__(self, request: Request) -> Optional[str]:
        from fastapi.security.utils import get_authorization_scheme_param
        authorization = request.headers.get('Authorization')
        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != 'bearer':
            if self.auto_error:
                raise self.make_not_authenticated_error()
            else:
                return None
        return param


oauth2_scheme = ClientCredentialsBearer(
    tokenUrl='v1/auth/token',
    refreshUrl='v1/auth/token/refresh',
    scopes=Permissions.scopes,
    auto_error=False,
)
http_basic_scheme = HTTPBasic()


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    from datetime import timezone
    from app import config

    to_encode = data.copy()
    expire = datetime.now(tz=timezone.utc) + (expires_delta or timedelta(seconds=ACCESS_TOKEN_AGE))
    to_encode.update({"exp": int(expire.timestamp())})

    return jwt.encode(to_encode, config.app.secret_key, algorithm=ALGORITHM)
