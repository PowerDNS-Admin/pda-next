from fastapi import APIRouter
from app.routers import router_responses

router = APIRouter(
    prefix='/dev',
    tags=['dev'],
    responses=router_responses,
)
