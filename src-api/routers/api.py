from fastapi import APIRouter
from routers.root import router_responses
from routers.v1 import router as v1_router

router = APIRouter(
    prefix='/api',
    responses=router_responses,
)

# Setup descendent routers
router.include_router(v1_router)
