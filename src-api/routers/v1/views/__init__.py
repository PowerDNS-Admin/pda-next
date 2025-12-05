from fastapi import APIRouter

from routers.root import router_responses

router = APIRouter(
    prefix='/views',
    tags=['views'],
    responses=router_responses,
)


from .views import *
from .networks import *
from .zones import *
