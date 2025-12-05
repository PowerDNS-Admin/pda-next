from typing import Optional

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from lib.api.dependencies import get_db_session, get_principal
from models.api import UsersSchema, ListParamsModel, Principal, UserSchema, UserAuthenticatorsSchema, \
    UserAuthenticatorSchema
from routers.v1.auth import router


@router.post(
    '/users',
    response_model=UsersSchema,
    summary='Get Users',
    description='Get all users in the current context.',
)
async def list_users(
        params: Optional[ListParamsModel] = None,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
) -> UsersSchema:
    """Gets all users in the current context."""
    from sqlalchemy import select, func
    from lib.sql import SqlQueryBuilder
    from models.db.auth import User

    stmt = select(User)

    if principal.tenant_id:
        stmt = stmt.where(User.tenant_id == principal.tenant_id)

    stmt_count = select(func.count()).select_from(stmt.subquery())

    if params:
        stmt = SqlQueryBuilder.apply_params(params, stmt, User)

    records = (await session.execute(stmt)).scalars().all()

    result = UsersSchema(
        records=[UserSchema.model_validate(r) for r in records],
        total=(await session.execute(stmt_count)).scalar_one(),
    )

    return result


@router.post(
    '/users/authenticators',
    response_model=UserAuthenticatorsSchema,
    summary='Get User Authenticators',
    description='Get all user authenticators in the current context.',
)
async def list_user_authenticators(
        params: Optional[ListParamsModel] = None,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
) -> UserAuthenticatorsSchema:
    """Gets all user authenticators in the current context."""
    from sqlalchemy import select, func
    from lib.sql import SqlQueryBuilder
    from models.db.auth import UserAuthenticator

    stmt = select(UserAuthenticator)

    if principal.tenant_id:
        stmt = stmt.where(UserAuthenticator.tenant_id == principal.tenant_id)

    stmt_count = select(func.count()).select_from(stmt.subquery())

    if params:
        stmt = SqlQueryBuilder.apply_params(params, stmt, UserAuthenticator)

    records = (await session.execute(stmt)).scalars().all()

    result = UserAuthenticatorsSchema(
        records=[UserAuthenticatorSchema.model_validate(r) for r in records],
        total=(await session.execute(stmt_count)).scalar_one(),
    )

    return result
