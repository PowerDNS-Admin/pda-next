from fastapi import APIRouter
from app.routers import router_responses
from app.routers.v1.services import mail

router = APIRouter(
    prefix='/services',
    responses=router_responses,
)

# Setup descendent routers
router.include_router(mail.router)
