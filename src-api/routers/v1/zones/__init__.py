from fastapi import APIRouter

from routers.root import router_responses

router = APIRouter(
    prefix='/zones',
    tags=['zones'],
    responses=router_responses,
)


from .azones import *
from .azone_records import *
from .azone_metadata import *
from .rzones import *
from .rzone_records import *
