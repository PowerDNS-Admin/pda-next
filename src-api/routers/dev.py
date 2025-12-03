from uuid import UUID

from fastapi import APIRouter, Request, Depends, Security
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from lib.api.dependencies import get_db_session, get_principal, require_permission
from lib.permissions.definitions import Permissions as p, Permission
from models.api.auth import Principal
from models.enums import ResourceTypeEnum
from routers.root import router_responses

router = APIRouter(
    prefix='/dev',
    tags=['dev'],
    responses=router_responses,
)


@router.get('/proxy/test')
async def proxy_test(request: Request) -> JSONResponse:
    return JSONResponse({
        'host': request.headers.get('Host'),
        'client-host': request.client.host,
        'x-real-ip': request.headers.get('X-Real-IP'),
        'x-forwarded-for': request.headers.get('X-Forwarded-For'),
        'x-forwarded-proto': request.headers.get('X-Forwarded-Proto'),
        'x-forwarded-host': request.headers.get('X-Forwarded-Host'),
        'x-forwarded-prefix': request.headers.get('X-Forwarded-Prefix'),
        'root_path': request.scope.get('root_path'),
        'request_path': request.url.path,
    })


@router.get(
    '/db/schema',
    summary='Creates Database Schema',
    description='This provides the ability to drop and/or create missing database schemas.',
)
async def db_schema(drop: bool = False, create:bool = True) -> JSONResponse:
    from loguru import logger
    from app import db_engine
    from models.db import BaseSqlModel

    tables = BaseSqlModel.metadata.tables.keys()

    async with db_engine.begin() as conn:
        if drop:
            logger.warning(f'Dropping Database Tables: {", ".join(tables)}')
            await conn.run_sync(BaseSqlModel.metadata.drop_all)

        if create:
            logger.warning(f'Creating Database Tables: {", ".join(tables)}')
            await conn.run_sync(BaseSqlModel.metadata.create_all)

        if drop or create:
            await conn.commit()

    return JSONResponse({'result': 'Database Schema Created!'})


@router.get(
    '/settings/default',
    summary='Reset system-level settings',
    description="Resets the system-level settings in the database with the defined defaults.",
)
async def settings_default(session: AsyncSession = Depends(get_db_session)) -> JSONResponse:
    """Temporary route for testing settings."""
    from lib.settings import SettingsManager

    total_created = await SettingsManager.default_settings(session)

    return JSONResponse({'total_created': total_created})


@router.get(
    '/settings/create-missing',
    summary='Load database with missing settings',
    description="Loads the database with any system settings that don't already exist.",
)
async def settings_create_missing(session: AsyncSession = Depends(get_db_session)) -> JSONResponse:
    """Temporary route for testing settings."""
    from lib.settings import SettingsManager

    total_created = await SettingsManager.create_settings(session)

    return JSONResponse({'total_created': total_created})


@router.get(
    '/test/data',
    summary='Loads the database with test data',
    description="Loads the database with test data.",
)
async def test_data(session: AsyncSession = Depends(get_db_session)) -> JSONResponse:
    """Temporary route for testing settings."""
    from datetime import datetime, timedelta, timezone
    from uuid import uuid4
    from lib.permissions.definitions import Permissions as p
    from models.db.acl import Role, RolePrincipal, RolePermission
    from models.db.auth import User, Client
    from models.db.system import StopgapDomain
    from models.db.tenants import Tenant
    from models.db.zones import AZone, AZoneRecord
    from models.enums import PrincipalTypeEnum, UserStatusEnum, AZoneKindEnum, ZoneRecordTypeEnum

    client_expires = datetime.now(tz=timezone.utc) + timedelta(days=7)

    # Create Stopgap Domain
    sg_domain = StopgapDomain(
        id=uuid4(),
        name='SG Test Domain 1',
        fqdn='local.powerdnsadmin.org',
        restricted_hosts=['admin', 'owner', 'root'],
    )

    session.add(sg_domain)

    # Create a system-level client
    sl_client = Client(
        id=uuid4(),
        name='System-Level Test Client',
        scopes=[
            p.auth_users.uri,
            p.acl_roles.uri,
        ],
        expires_at=client_expires,
    )
    sl_client.secret = 'test'

    session.add(sl_client)

    # Create a system-level user
    sl_user = User(
        id=uuid4(),
        username='test',
        status=UserStatusEnum.active,
    )
    sl_user.password = 'test'

    session.add(sl_user)

    # Create a system-level user client
    sl_user_client = Client(
        id=uuid4(),
        user_id=sl_user.id,
        name='System-Level Test User Client',
        scopes=[
            p.auth_users_read.uri,
            p.auth_users_create.uri,
            p.acl_roles_read.uri,
            p.acl_roles_create.uri,
        ],
        expires_at=client_expires,
    )
    sl_user_client.secret = 'test'

    session.add(sl_user_client)

    sl_role = Role(
        id=uuid4(),
        slug='system-admin',
        description='A role for system administrators with full access.',
    )

    session.add(sl_role)

    sl_role_permission = RolePermission(
        role_id=sl_role.id,
        permission=p.auth_users.uri,
    )

    session.add(sl_role_permission)

    sl_role_permission = RolePermission(
        role_id=sl_role.id,
        permission=p.tenants_read.uri,
    )

    session.add(sl_role_permission)

    sl_role_principal = RolePrincipal(
        role_id=sl_role.id,
        principal_type=PrincipalTypeEnum.client,
        principal_id=sl_client.id,
    )

    session.add(sl_role_principal)

    # Create tenants
    tenant1 = Tenant(
        id=uuid4(),
        name='Test Tenant 1',
        stopgap_domain_id=sg_domain.id,
        stopgap_hostname='t1',
    )

    session.add(tenant1)

    tenant2 = Tenant(
        id=uuid4(),
        name='Test Tenant 2',
        fqdn='local.dnsmin.org',
    )

    session.add(tenant2)

    # Create a tenant-level client

    tl_client1 = Client(
        id=uuid4(),
        tenant_id=tenant1.id,
        name='Tenant-Level Test Client 1',
        scopes=[
            p.auth_users.uri,
            p.acl_roles.uri,
            p.zones_azone.uri,
            p.zones_azone_read.uri,
            p.zones_rzone.uri,
            p.zones_rzone_read.uri,
        ],
        expires_at=client_expires,
    )
    tl_client1.secret = 'test'

    session.add(tl_client1)

    tl_client2 = Client(
        id=uuid4(),
        tenant_id=tenant2.id,
        name='Tenant-Level Test Client 2',
        scopes=[
            p.auth_users.uri,
            p.acl_roles.uri,
        ],
        expires_at=client_expires,
    )
    tl_client2.secret = 'test'

    session.add(tl_client2)

    # Create a tenant-level user
    tl_user = User(
        id=uuid4(),
        tenant_id=tenant1.id,
        username='test',
        status=UserStatusEnum.active,
    )
    tl_user.password = 'test'

    session.add(tl_user)

    # Create a tenant-level user client
    tl_user_client = Client(
        id=uuid4(),
        tenant_id=tenant1.id,
        user_id=tl_user.id,
        name='Tenant-Level Test User Client',
        scopes=[
            p.auth_users_read.uri,
            p.auth_users_create.uri,
            p.acl_roles_read.uri,
            p.acl_roles_create.uri,
        ],
        expires_at=client_expires,
    )
    tl_user_client.secret = 'test'

    session.add(tl_user_client)

    tl_role1 = Role(
        id=uuid4(),
        tenant_id=tenant1.id,
        slug='tenant-admin',
        description='A role for tenant system administrators with full access.',
    )

    session.add(tl_role1)

    tl_role_permission = RolePermission(
        role_id=tl_role1.id,
        permission=p.auth_users.uri,
    )

    session.add(tl_role_permission)

    tl_role_permission = RolePermission(
        role_id=tl_role1.id,
        permission=p.tenants.uri,
    )

    session.add(tl_role_permission)

    tl_role_principal = RolePrincipal(
        role_id=tl_role1.id,
        tenant_id=tenant1.id,
        principal_type=PrincipalTypeEnum.client,
        principal_id=tl_client1.id,
    )

    session.add(tl_role_principal)

    tl_role1 = Role(
        id=uuid4(),
        tenant_id=tenant1.id,
        slug='zone-admin',
        description='A role for tenant zone administrators with full access.',
    )

    session.add(tl_role1)

    tl_role_permission = RolePermission(
        role_id=tl_role1.id,
        permission=p.zones_azone_read.uri,
    )

    session.add(tl_role_permission)

    tl_role_permission = RolePermission(
        role_id=tl_role1.id,
        permission=p.zones_rzone_read.uri,
    )

    session.add(tl_role_permission)

    tl_role_principal = RolePrincipal(
        role_id=tl_role1.id,
        tenant_id=tenant1.id,
        principal_type=PrincipalTypeEnum.client,
        principal_id=tl_client1.id,
    )

    session.add(tl_role_principal)

    tl_role2 = Role(
        id=uuid4(),
        tenant_id=tenant2.id,
        slug='tenant-admin',
        description='A role for tenant system administrators with full access.',
    )

    session.add(tl_role2)

    tl_role_permission = RolePermission(
        role_id=tl_role2.id,
        permission=p.auth_users.uri,
    )

    session.add(tl_role_permission)

    tl_role_permission = RolePermission(
        role_id=tl_role2.id,
        permission=p.tenants_read.uri,
    )

    session.add(tl_role_permission)

    tl_role_principal = RolePrincipal(
        role_id=tl_role2.id,
        principal_type=PrincipalTypeEnum.client,
        principal_id=tl_client2.id,
    )

    session.add(tl_role_principal)

    tl_t1_zone1 = AZone(
        id=uuid4(),
        tenant_id=tenant1.id,
        fqdn='azorian.solutions',
        kind=AZoneKindEnum.MASTER,
        serial=123456789,
        notified_serial=123456789,
        edited_serial=123456789,
    )

    session.add(tl_t1_zone1)

    tl_t1_zone1_r1 = AZoneRecord(
        id=uuid4(),
        tenant_id=tenant1.id,
        zone_id=tl_t1_zone1.id,
        name='',
        type_=ZoneRecordTypeEnum.A,
        ttl=3600,
        content='1.1.1.1',
    )

    session.add(tl_t1_zone1_r1)
    
    await session.commit()

    return JSONResponse({
        'system-level-role': sl_role.id.hex,
        'system-level-client': sl_client.id.hex,
        'system-level-user': sl_user.id.hex,
        'system-level-user-client': sl_user_client.id.hex,
        'tenant': tenant1.id.hex,
        'tenant-level-role1': tl_role1.id.hex,
        'tenant-level-client1': tl_client1.id.hex,
        'tenant-level-user': tl_user.id.hex,
        'tenant-level-user-client': tl_user_client.id.hex,
        'tenant-level-role2': tl_role2.id.hex,
        'tenant-level-client2': tl_client2.id.hex,
    })


@router.get('/auth/principal', response_model=Principal)
async def auth_principal(principal: Principal = Depends(get_principal)) -> Principal:
    return principal


@router.get(
    '/acl/test/zones/{zone_id}',
    response_model=Principal,
    summary='Tests permission system.',
    description='This provides a testing circuit for the permissions system.',
)
async def acl_test(
        zone_id: str,
        principal: Principal = Depends(get_principal),
        _=Depends(require_permission(
            ResourceTypeEnum.zones_azone,
            'zone_id',
            p.zones_azone_read,
        )),
) -> Principal:
    return principal
