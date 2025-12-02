from fastapi import APIRouter

from routers.root import router_responses
from routers.v1 import auth, acl, settings, system, tenants, servers, keys, zones, views, tasks, services

router = APIRouter(
    prefix='/v1',
    responses=router_responses,
)

# Setup descendent routers
router.include_router(auth.router)
router.include_router(acl.router)
router.include_router(settings.router)
router.include_router(system.router)
router.include_router(tenants.router)
router.include_router(servers.router)
router.include_router(keys.router)
router.include_router(zones.router)
router.include_router(views.router)
router.include_router(tasks.router)
router.include_router(services.router)
