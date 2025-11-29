from fastapi import APIRouter, Form, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from lib.api.dependencies import get_db_session
from routers.root import router_responses
from routers.v1 import auth, services, tasks

router = APIRouter(
    prefix='/v1',
    responses=router_responses,
)

# Setup descendent routers
router.include_router(auth.router)
router.include_router(services.router)
router.include_router(tasks.router)


@router.post('/token')
async def token(
        grant_type: str = Form(...),
        client_id: str = Form(...),
        client_secret: str = Form(...),
        username: str = Form(None),
        password: str = Form(None),
        refresh_token: str = Form(None),
        session: AsyncSession = Depends(get_db_session),
):
    """Handle OAuth token grants."""
    from lib.security import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, TokenGrantTypeEnum
    from models.db.auth import Client, RefreshToken, User

    # Validate Client
    client = await Client.get_by_id(session, client_id)
    if not client or not client.verify_secret(client_secret):
        raise HTTPException(400, 'invalid_client')

    # Client Credential Grants
    if grant_type == TokenGrantTypeEnum.client_credentials.value:
        access = create_access_token({'sub': f'client:{client_id}'})
        refresh = await RefreshToken.create_token(session, client_id)

        return {
            'access_token': access,
            'token_type': 'bearer',
            'expires_in': ACCESS_TOKEN_EXPIRE_MINUTES,
            'refresh_token': str(refresh.id),
        }

    # Username Credential Grants
    if grant_type == TokenGrantTypeEnum.password.value:
        user = await User.get_by_username(session, username)
        if not user or not user.verify_password(password):
            raise HTTPException(400, 'invalid_user')

        access = create_access_token({'sub': str(user.id)})
        refresh = await RefreshToken.create_token(session, client_id, str(user.id))

        return {
            'access_token': access,
            'token_type': 'bearer',
            'expires_in': ACCESS_TOKEN_EXPIRE_MINUTES,
            'refresh_token': str(refresh.id),
        }

    # Refresh Token Grants
    if grant_type == TokenGrantTypeEnum.refresh_token.value:
        stored = await RefreshToken.get_by_id(session, refresh_token)
        if not stored or stored.revoked or stored.client_id != client_id:
            raise HTTPException(400, 'invalid_grant')

        await RefreshToken.revoke_token(session, stored)

        access = create_access_token({'sub': str(stored.user_id) if stored.user_id else f'client:{client_id}'})
        refresh = await RefreshToken.create_token(session, client_id, str(stored.user_id))

        return {
            'access_token': access,
            'token_type': 'bearer',
            'expires_in': ACCESS_TOKEN_EXPIRE_MINUTES,
            'refresh_token': str(refresh.id),
        }

    raise HTTPException(400, 'unsupported_grant_type')
