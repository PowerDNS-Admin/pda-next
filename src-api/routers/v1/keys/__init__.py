from fastapi import APIRouter

from routers.root import router_responses

router = APIRouter(
    prefix='/keys',
    tags=['keys'],
    responses=router_responses,
)


from .crypto import *
from .tsig import *
