from fastapi import APIRouter
from fastapi.responses import JSONResponse, RedirectResponse
from lib.pda.api import NotFoundResponse, StatusResponse

# Define generic responses to be used by routers
router_responses: dict = {
    404: {'model': NotFoundResponse},
}

router = APIRouter(
    prefix='/api',
    responses=router_responses,
)


@router.get('', response_class=RedirectResponse)
async def root() -> RedirectResponse:
    return RedirectResponse(url='/api/docs')


@router.get('/', response_class=RedirectResponse)
async def root() -> RedirectResponse:
    return RedirectResponse(url='/api/docs')


@router.get('/status', response_model=StatusResponse)
async def status() -> JSONResponse:
    response: StatusResponse = StatusResponse()
    return JSONResponse(response.model_dump(mode='json'))
