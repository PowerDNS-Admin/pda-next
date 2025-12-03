from typing import AsyncGenerator, Callable
from uuid import UUID

from fastapi import Depends, Request, Form, HTTPException, status
from fastapi.security import HTTPBasicCredentials, SecurityScopes
from sqlalchemy.orm import Mapped
from sqlalchemy.ext.asyncio import AsyncSession

from lib.api.oauth import oauth2_scheme, http_basic_scheme
from lib.permissions.manager import PermissionsManager
from lib.permissions.definitions import Permission
from models.api.auth import Principal
from models.enums import ResourceTypeEnum


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    from app import AsyncSessionLocal
    async with AsyncSessionLocal() as session:
        yield session


async def get_principal(
        request: Request,
        session: AsyncSession = Depends(get_db_session),
        bearer_token: str = Depends(oauth2_scheme),
) -> Principal:
    from datetime import datetime, timezone
    from typing import Optional
    from jose import JWTError, jwt
    from loguru import logger
    from app import config
    from lib.security import ALGORITHM, TENANT_HEADER_NAME
    from lib.settings import SettingsManager
    from lib.settings.definitions import sd
    from lib.tenants import TenantManager
    from models.db.auth import Session, Client
    from models.enums import PrincipalTypeEnum

    tenant_id: Optional[UUID] = None

    # Attempt to identity the tenant by header
    if TENANT_HEADER_NAME in request.headers:
        try:
            tenant_id = UUID(request.headers[TENANT_HEADER_NAME])
        except ValueError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid Tenant ID')

    # Attempt to identify the tenant by hostname if not provided by request header
    if not isinstance(tenant_id, UUID):
        tenant_id = await TenantManager.get_tenant_id_by_fqdn(session, request.headers.get('host'))

    # Attempt OAuth Bearer Token Authentication
    if bearer_token:
        invalid_token_msg = 'Invalid bearer token'
        try:
            payload = jwt.decode(bearer_token, config.app.secret_key, algorithms=[ALGORITHM])
        except JWTError:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, invalid_token_msg)

        if 'sub' not in payload or 'exp' not in payload:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, invalid_token_msg)

        client = await Client.get_by_id(session, payload['sub'])

        if not client:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, invalid_token_msg)

        # Verify that token hasn't expired
        if datetime.now(timezone.utc) > datetime.fromtimestamp(payload['exp'], tz=timezone.utc):
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, invalid_token_msg)

        # Verify that the client matches the associated tenant of the request if any
        if isinstance(client.tenant_id, UUID) and not isinstance(tenant_id, UUID) \
                or not isinstance(client.tenant_id, UUID) and isinstance(tenant_id, UUID) \
                or client.tenant_id != tenant_id:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, 'Wrong access configuration')

        principal = Principal(id=client.id, tenant_id=tenant_id, type=PrincipalTypeEnum.client)

        if 'scope' in payload:
            principal.permissions = set(payload['scope'].split(' '))

        return principal

    cookie_name = (await SettingsManager.get(session=session, key=sd.auth_session_cookie_name.key)).value

    # Attempt Session Token Authentication
    session_token = request.cookies.get(cookie_name)
    if session_token:
        # TODO: Implement hijack detection failsafe and terminate session if token matches but remote IP doesn't
        db_session = await Session.get_by_token(session, session_token, request.client.host)
        if db_session:
            # Verify that the associated user matches the tenant associated with the request if any
            if isinstance(db_session.user.tenant_id, UUID) and not isinstance(tenant_id, UUID) \
                    or not isinstance(db_session.user.tenant_id, UUID) and isinstance(tenant_id, UUID) \
                    or db_session.user.tenant_id != tenant_id:
                raise HTTPException(status.HTTP_401_UNAUTHORIZED, 'Wrong access configuration')

            # Extend the session's expiration timestamp
            await Session.extend_session(session, db_session)

            # TODO: Load the user's permissions into the principal

            return Principal(id=db_session.user.id, tenant_id=tenant_id, type=PrincipalTypeEnum.user)

    # If neither works, raise an exception
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Not authenticated'
    )


def require_permission(
        resource_type: ResourceTypeEnum,
        resource_id_param_name: str,
        permissions: Permission | list[Permission],
) -> Callable:
    """Enforces the given permissions against the current principal's permissions for the given resource."""

    async def dep(
            request: Request,
            principal: Principal = Depends(get_principal),
            db: AsyncSession = Depends(get_db_session),
    ):
        resource_id = request.path_params.get(resource_id_param_name)
        if resource_id is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'Missing {resource_id_param_name}')
        if await PermissionsManager.has_permission(db, principal, resource_type, resource_id, permissions):
            return True
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Missing permissions')

    return dep


async def authorize_oauth_client(
        credentials: HTTPBasicCredentials = Depends(http_basic_scheme),
        grant_type: str = Form(...),
        scope: str = Form(None),
        session: AsyncSession = Depends(get_db_session),
) -> UUID | Mapped[UUID]:
    from lib.security import TokenGrantTypeEnum, TokenErrorTypeEnum
    from models.db.auth import Client

    # Standard OAuth requires the grant_type field to be present in the body
    if grant_type != TokenGrantTypeEnum.client_credentials.value:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Invalid grant_type provided. Must be "client_credentials".'
        )

    # Retrieve the referenced client
    client = await Client.get_by_id(session, credentials.username)

    # Validate the client
    if not client or not client.verify_secret(credentials.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=TokenErrorTypeEnum.invalid_client.value,
            headers={'WWW-Authenticate': 'Bearer'},
        )

    # Validate the requested scopes
    granted_scopes = set(client.scopes if client.scopes else [])
    required_scopes = set(scope.split(' ') if scope else [])

    if not required_scopes.issubset(granted_scopes):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=TokenErrorTypeEnum.missing_required_scopes.value,
            headers={'WWW-Authenticate': 'Bearer'},
        )

    # Return the client schema upon successful validation
    return client.id
