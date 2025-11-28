from fastapi import APIRouter
from app.routers import router_responses
from app.routers.v1 import dev, services, tasks

router = APIRouter(
    prefix='/v1',
    responses=router_responses,
)

# Setup descendent routers
# router.include_router(dev.router)
router.include_router(services.router)
router.include_router(tasks.router)
