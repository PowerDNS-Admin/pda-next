from fastapi import APIRouter

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
