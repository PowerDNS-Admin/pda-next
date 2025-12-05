from fastapi import Depends

from lib.api.dependencies import get_principal
from models.api import Principal
from models.api.acl.metadata import PermissionsMetadataSchema
from routers.v1.acl import router


@router.get(
    '/metadata',
    response_model=PermissionsMetadataSchema,
    summary='Retrieve Permissions Metadata',
    description='Retrieves all ACL permissions metadata.',
    operation_id='acl:metadata:all',
)
async def list_metadata(
        principal: Principal = Depends(get_principal),
) -> PermissionsMetadataSchema:
    """List ACL permissions metadata."""
    return PermissionsMetadataSchema()
