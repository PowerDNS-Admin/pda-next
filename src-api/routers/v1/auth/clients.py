from typing import Optional

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from lib.api.dependencies import get_db_session, get_principal
from models.api import ClientsSchema, ListParamsModel, Principal, ClientSchema
from routers.v1.auth import router


@router.post(
    '/clients',
    response_model=ClientsSchema,
    summary='Get Clients',
    description='Get all clients in the current context.',
)
async def list_clients(
        params: Optional[ListParamsModel] = None,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
) -> ClientsSchema:
    """Gets all clients in the current context."""
    from sqlalchemy import select, func
    from lib.sql import SqlQueryBuilder
    from models.db.auth import Client

    stmt = select(Client)

    if principal.tenant_id:
        stmt = stmt.where(Client.tenant_id == principal.tenant_id)

    stmt_count = select(func.count()).select_from(stmt.subquery())

    if params:
        stmt = SqlQueryBuilder.apply_params(params, stmt, Client)

    records = (await session.execute(stmt)).scalars().all()

    result = ClientsSchema(
        records=[ClientSchema.model_validate(r) for r in records],
        total=(await session.execute(stmt_count)).scalar_one(),
    )

    return result
