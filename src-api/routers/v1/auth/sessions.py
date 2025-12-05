from typing import Optional

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from lib.api.dependencies import get_db_session, get_principal
from models.api import SessionsSchema, ListParamsModel, Principal, SessionSchema
from routers.v1.auth import router


@router.post(
    '/sessions',
    response_model=SessionsSchema,
    summary='Get User Sessions',
    description='Get all user sessions in the current context.',
)
async def list_sessions(
        params: Optional[ListParamsModel] = None,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
) -> SessionsSchema:
    """Gets all user sessions in the current context."""
    from sqlalchemy import select, func
    from lib.sql import SqlQueryBuilder
    from models.db.auth import Session

    stmt = select(Session)

    if principal.tenant_id:
        stmt = stmt.where(Session.tenant_id == principal.tenant_id)

    stmt_count = select(func.count()).select_from(stmt.subquery())

    if params:
        stmt = SqlQueryBuilder.apply_params(params, stmt, Session)

    records = (await session.execute(stmt)).scalars().all()

    result = SessionsSchema(
        records=[SessionSchema.model_validate(r) for r in records],
        total=(await session.execute(stmt_count)).scalar_one(),
    )

    return result
