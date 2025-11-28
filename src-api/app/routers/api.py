from fastapi import APIRouter
from app.routers import router_responses
from app.routers.v1 import router as v1_router

router = APIRouter(
    prefix='/api',
    responses=router_responses,
)

# Setup descendent routers
router.include_router(v1_router)
