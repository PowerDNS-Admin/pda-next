from typing import Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession


class TenantManager:
    """Provides an interface for managing and interacting with tenant data."""

    @staticmethod
    async def get_tenant_id_by_fqdn(session: AsyncSession, fqdn: Optional[str]) -> Optional[UUID]:
        """Retrieves a tenant ID by associated FQDN."""
        from sqlalchemy import select
        from models.db.system import StopgapDomain
        from models.db.tenants import Tenant

        if not isinstance(fqdn, str):
            return None

        # Attempt to identify tenant by associated FQDN
        stmt = select(Tenant.id).where(Tenant.fqdn == fqdn)

        tenant_id = (await session.execute(stmt)).scalar_one_or_none()

        if isinstance(tenant_id, UUID):
            return tenant_id

        # Attempt to identify tenant by associated stopgap domain if not found by FQDN
        fqdn_parts = fqdn.split('.', 1)
        hostname = fqdn_parts[0]
        stopgap_domain = fqdn_parts[1]

        stmt = select(StopgapDomain.id).where(StopgapDomain.fqdn == stopgap_domain)
        stopgap_domain_id = (await session.execute(stmt)).scalar_one_or_none()

        if not isinstance(stopgap_domain_id, UUID):
            return None

        stmt = select(Tenant.id).where(
            Tenant.stopgap_domain_id == stopgap_domain_id, Tenant.stopgap_hostname == hostname
        )

        return (await session.execute(stmt)).scalar_one_or_none()
