from fastapi import APIRouter
from routers.root import router_responses
from routers.v1.services import mail

router = APIRouter(
    prefix='/services',
    tags=['services'],
    responses=router_responses,
)

# Setup descendent routers
router.include_router(mail.router)
