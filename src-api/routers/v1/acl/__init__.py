from fastapi import APIRouter

from routers.root import router_responses

router = APIRouter(
    prefix='/acl',
    tags=['acl'],
    responses=router_responses,
)

from .roles import *
from .policies import *
