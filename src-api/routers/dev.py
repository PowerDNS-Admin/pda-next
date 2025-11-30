from fastapi import APIRouter, Request, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from lib.api.dependencies import get_db_session, get_principal
from models.api.auth import UserSchema, ClientSchema
from routers.root import router_responses

router = APIRouter(
    prefix='/dev',
    responses=router_responses,
)


@router.get('/proxy/test')
async def proxy_test(request: Request) -> JSONResponse:
    return JSONResponse({
        'host': request.headers.get('Host'),
        'client-host': request.client.host,
        'x-real-ip': request.headers.get('X-Real-IP'),
        'x-forwarded-for': request.headers.get('X-Forwarded-For'),
        'x-forwarded-proto': request.headers.get('X-Forwarded-Proto'),
        'x-forwarded-host': request.headers.get('X-Forwarded-Host'),
        'x-forwarded-prefix': request.headers.get('X-Forwarded-Prefix'),
        'root_path': request.scope.get('root_path'),
        'request_path': request.url.path,
    })


@router.get('/db/schema')
async def db_schema(drop: bool = False, create:bool = True) -> JSONResponse:
    from loguru import logger
    from app import db_engine
    from models.db import BaseSqlModel

    tables = BaseSqlModel.metadata.tables.keys()

    async with db_engine.begin() as conn:
        if drop:
            logger.warning(f'Dropping Database Tables: {", ".join(tables)}')
            await conn.run_sync(BaseSqlModel.metadata.drop_all)

        if create:
            logger.warning(f'Creating Database Tables: {", ".join(tables)}')
            await conn.run_sync(BaseSqlModel.metadata.create_all)

        if drop or create:
            await conn.commit()

    return JSONResponse({'result': 'Database Schema Created!'})


@router.get('/db/test')
async def db_test(session: AsyncSession = Depends(get_db_session)) -> JSONResponse:
    return JSONResponse({})


@router.get('/auth/create-client', response_model=ClientSchema)
async def auth_create_client(session: AsyncSession = Depends(get_db_session)) -> ClientSchema:
    """Creates an auth client."""
    import json
    from models.db.auth import Client

    db_client = Client(
        name='Test Client',
        scopes=json.dumps(['audit:*', 'zone:*']),
    )

    db_client.secret = 'testtest'

    session.add(db_client)
    await session.commit()
    await session.refresh(db_client)

    return ClientSchema.model_validate(db_client)


@router.get('/auth/create-user', response_model=UserSchema)
async def auth_create_user(session: AsyncSession = Depends(get_db_session)) -> UserSchema:
    """Creates an auth user."""
    from models.api.auth import UserSchema
    from models.db.auth import User
    from models.enums import UserStatusEnum

    db_user = User(
        username='test',
        status=UserStatusEnum.active,
    )

    db_user.password = 'testtest'

    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)

    return UserSchema.model_validate(db_user)


@router.get('/auth/test/client', response_model=UserSchema | ClientSchema)
async def auth_test_client(principal: UserSchema | ClientSchema = Depends(get_principal)) -> UserSchema | ClientSchema:
    from loguru import logger
    logger.warning(principal)
    return principal


@router.get('/auth/test/user', response_model=UserSchema | ClientSchema)
async def auth_test_user(principal: UserSchema | ClientSchema = Depends(get_principal)) -> UserSchema | ClientSchema:
    from loguru import logger
    logger.warning(principal)
    return principal


@router.get('/acl/test')
async def acl_test(principal: UserSchema | ClientSchema = Depends(get_principal)) -> JSONResponse:
    return JSONResponse(principal.model_dump(mode='json'))
