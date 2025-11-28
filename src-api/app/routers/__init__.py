from fastapi import FastAPI, APIRouter, Request
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.security import OAuth2PasswordBearer
from app.lib.pda.api import NotFoundResponse, StatusResponse

# Initialize Authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='api/v1/token')

# Define generic responses to be used by routers
router_responses: dict = {
    404: {'model': NotFoundResponse},
}

router = APIRouter(
    prefix='',
    responses=router_responses,
)


def install_routers(app: FastAPI) -> None:
    """Attach local and global routers"""
    from app.routers import api
    from app.routers import v1

    # API Router
    router.include_router(v1.router)

    # Root Router
    app.include_router(router)


@router.get('/', response_class=RedirectResponse)
async def root() -> RedirectResponse:
    return RedirectResponse(url='/docs')


@router.get('/status', response_model=StatusResponse)
async def status() -> JSONResponse:
    response: StatusResponse = StatusResponse()
    return JSONResponse(response.model_dump(mode='json'))


@router.get('/proxy-test')
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
