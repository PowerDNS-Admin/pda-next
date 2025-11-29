from fastapi import APIRouter, Request, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from lib.api.dependencies import get_db_session, get_principal
from models.api.auth import UserApi, ClientApi
from routers.root import router_responses

router = APIRouter(
    prefix='/dev',
    responses=router_responses,
)


@router.get('/proxy/test')
async def proxy_test(request: Request) -> JSONResponse:
    return JSONResponse({
        'host': request.headers.get('Host'),
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
    import importlib.util, os, sys
    from loguru import logger
    from app import db_engine, settings
    from models.db import BaseSqlModel

    models_dir = f'{settings.root_path}/src/models/db'

    if not os.path.isdir(models_dir):
        logger.warning(f'Models directory does not exist: {models_dir}')
        return JSONResponse({}, status_code=500)

    sys.path.append(os.path.abspath(os.path.dirname(models_dir)))

    for filename in os.listdir(models_dir):
        if filename.endswith(".py") and not filename.startswith("__"):
            # Construct module name without the .py extension
            module_name = filename[:-3]
            file_path = os.path.join(models_dir, filename)

            try:
                # Use importlib to dynamically load the module
                spec = importlib.util.spec_from_file_location(module_name, file_path)
                module = importlib.util.module_from_spec(spec)
                sys.modules[module_name] = module
                spec.loader.exec_module(module)
                logger.debug(f'Successfully loaded module: {module_name}')
            except Exception as e:
                logger.error(f'Failed to load module ({module_name}): {e}')

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


@router.get('/auth/create-client', response_model=ClientApi)
async def auth_create_client(session: AsyncSession = Depends(get_db_session)) -> ClientApi:
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

    return ClientApi.model_validate(db_client)


@router.get('/auth/create-user', response_model=UserApi)
async def auth_create_user(session: AsyncSession = Depends(get_db_session)) -> UserApi:
    """Creates an auth user."""
    from models.api.auth import UserApi
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

    return UserApi.model_validate(db_user)


@router.get('/auth/test/client')
async def auth_test_client(principal: UserApi | ClientApi = Depends(get_principal)) -> JSONResponse:
    from loguru import logger
    logger.warning(principal)
    return JSONResponse(principal.model_dump(mode='json'))


@router.get('/auth/test/user')
async def auth_test_user(principal: UserApi | ClientApi = Depends(get_principal)) -> JSONResponse:
    from loguru import logger
    logger.warning(principal)
    return JSONResponse(principal.model_dump(mode='json'))


@router.get('/acl/test')
async def acl_test(principal: UserApi | ClientApi = Depends(get_principal)) -> JSONResponse:
    return JSONResponse(principal.model_dump(mode='json'))
