from fastapi import APIRouter

from routers.root import router_responses

router = APIRouter(
    prefix='/system',
    tags=['system'],
    responses=router_responses,
)


from .stopgap_domains import *
from .timezones import *
