from datetime import datetime, date, time
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, computed_field
from sqlalchemy.ext.asyncio import AsyncSession

from models.db.settings import Setting as DbSetting
from models.enums import SettingTypeEnum


class SettingException(Exception):
    """A generic Setting related exception."""
    message: str = 'An unknown setting exception occurred.'
    """The exception's message."""

    key: Optional[str] = None
    """The key of the setting."""

    tenant_id: Optional[str | UUID] = None
    """The tenant id of the setting if any."""

    user_id: Optional[str | UUID] = None
    """The user id of the setting if any."""

    def __init__(
            self,
            message: str | None = None,
            key: Optional[str] = None,
            tenant_id: Optional[str | UUID] = None,
            user_id: Optional[str | UUID] = None,
    ):
        self.message = message
        self.key = key
        self.tenant_id = tenant_id
        self.user_id = user_id
        super().__init__(message)


class SettingExistsException(SettingException):
    """An exception raised when attempting to create a setting that already exists."""
    message: str = 'Setting already exists!'
    """The exception's message."""


class SettingMissingException(SettingException):
    """An exception raised when attempting to update a setting that does not exist."""
    message: str = 'Setting does not exist!'
    """The exception's message."""


class Setting(BaseModel):
    """Provides an interface for defining a system setting and applying it accordingly."""
    model_config = ConfigDict(from_attributes=True)

    title: str = Field(
        title='Setting Title',
        description='The title of this setting.',
    )
    """The title of this setting."""

    description: str = Field(
        title='Setting Description',
        description='The description of this setting.',
    )
    """The description this setting."""

    key: str = Field(
        title='Setting Key',
        description='The key of this setting.',
    )
    """The key of this setting."""

    data_type: SettingTypeEnum = Field(
        title='Setting Data Type',
        description="The data type of this setting's value.",
    )
    """The data type of this setting's value."""

    raw_value: Optional[str] = Field(
        title='Setting Data Raw Value',
        description="The raw value of this setting.",
        default=None,
    )
    """The raw value of this setting."""

    default_value: str | int | float | bool | datetime | date | time | tuple | list | dict = Field(
        title='Setting Default Value',
        description='The default value of this setting.',
    )
    """The default value of this setting."""

    overridable: bool = Field(
        title='Setting Overridable',
        description='Whether the setting can be overridden in lower contexts.',
        default=False,
    )
    """Whether the setting can be overridden in lower contexts."""

    hidden: bool = Field(
        title='Setting Hidden',
        description='Whether the setting is hidden in lower contexts.',
        default=False,
    )
    """Whether the setting is hidden in lower contexts."""

    readonly: bool = Field(
        title='Setting Read-Only',
        description='Whether the setting can be modified in non-system contexts.',
        default=False,
    )
    """Whether the setting can be modified in non-system contexts."""

    @computed_field(
        title='Setting Value',
        description='The value of the setting.',
    )
    @property
    def value(self) -> str | int | float | bool | datetime | date | time | tuple | list | dict | None:
        """The value of the setting."""
        import json

        if self.raw_value is None:
            return None

        match self.data_type:
            case SettingTypeEnum.str:
                return str(self.raw_value)
            case SettingTypeEnum.int:
                return int(self.raw_value)
            case SettingTypeEnum.float:
                return float(self.raw_value)
            case SettingTypeEnum.bool:
                return bool(self.raw_value.lower())
            case SettingTypeEnum.datetime:
                return datetime.fromisoformat(self.raw_value)
            case SettingTypeEnum.date:
                return date.fromisoformat(self.raw_value)
            case SettingTypeEnum.time:
                return time.fromisoformat(self.raw_value)
            case SettingTypeEnum.tuple:
                return tuple(json.loads(self.raw_value))
            case SettingTypeEnum.list:
                return json.loads(self.raw_value)
            case SettingTypeEnum.dict:
                return json.loads(self.raw_value)
            case _:
                raise ValueError(f'Unknown setting type: {self.data_type}')

    @value.setter
    def value(self, value: str | int | float | bool | datetime | date | time | tuple | list | dict | None):
        """Sets the value of the setting."""
        import json

        value_type = type(value)

        if value is None:
            self.raw_value = None
        elif value_type in (str, int, float):
            self.raw_value = str(value)
        elif value_type == bool:
            self.raw_value = str(value).lower()
        elif value_type in (tuple, list, dict):
            self.raw_value = json.dumps(value)
        elif value_type in (datetime, date, time):
            self.raw_value = value.isoformat()
        else:
            raise ValueError(f'Unknown setting type: {value_type}')


class SettingsManager:
    """Provides an interface for managing system settings."""

    @staticmethod
    async def default_settings(session: AsyncSession) -> int:
        """
        Resets database-stored system level settings to the default values from the settings definition and returns
        the total created.
        """
        from loguru import logger
        from sqlalchemy import delete
        from lib.settings.definitions import sd

        definitions = list(dict(sd).values())

        stmt = delete(DbSetting).where(DbSetting.tenant_id == None, DbSetting.user_id == None)

        await session.execute(stmt)
        await session.commit()

        total_created = 0

        for setting in definitions:
            session.add(DbSetting(
                key=setting.key,
                raw_value=setting.default_value,
                overridable=setting.overridable,
                hidden=setting.hidden,
                readonly=setting.readonly,
            ))

            logger.trace(f'Creating setting: {setting.key}')

            total_created += 1

        await session.commit()

        return total_created

    @staticmethod
    async def create_settings(session: AsyncSession) -> int:
        """Creates defined settings that aren't currently in the database and returns the total created."""
        from loguru import logger
        from sqlalchemy import select
        from lib.settings.definitions import sd

        definitions = list(dict(sd).values())

        stmt = select(DbSetting.key).where(DbSetting.tenant_id == None, DbSetting.user_id == None)

        db_keys = set((await session.execute(stmt)).scalars().all())

        total_created = 0

        for setting in definitions:
            if setting.key in db_keys:
                continue

            session.add(DbSetting(
                key=setting.key,
                raw_value=setting.default_value,
                overridable=setting.overridable,
                hidden=setting.hidden,
                readonly=setting.readonly,
            ))

            logger.trace(f'Creating setting: {setting.key}')

            total_created += 1

        await session.commit()

        return total_created

    @staticmethod
    async def get_by_id(session: AsyncSession, id: str | UUID) -> DbSetting | None:
        """Retrieves a setting object by its id."""
        from sqlalchemy import select
        if isinstance(id, str):
            id = UUID(id)
        stmt = select(DbSetting).where(DbSetting.id == id)
        return (await session.execute(stmt)).scalar_one_or_none()

    @staticmethod
    async def get(
            session: AsyncSession,
            key: str,
            tenant_id: Optional[str | UUID] = None,
            user_id: Optional[str | UUID] = None,
            include_none: bool = False,
    ) -> Setting | None:
        """Retrieves a setting object by its key and optionally tenant and/or user id."""
        from sqlalchemy import select
        from lib.settings.definitions import sdk

        if isinstance(tenant_id, str):
            tenant_id = UUID(tenant_id)
        if isinstance(user_id, str):
            user_id = UUID(user_id)

        stmt = select(DbSetting).where(DbSetting.key == key)

        if include_none or isinstance(tenant_id, UUID):
            stmt = stmt.where(DbSetting.tenant_id == tenant_id)

        if include_none or isinstance(user_id, UUID):
            stmt = stmt.where(DbSetting.user_id == user_id)

        db_setting: DbSetting = (await session.execute(stmt)).scalar_one_or_none()

        if not db_setting:
            return None

        if db_setting.key not in sdk:
            return None

        setting = sdk[db_setting.key].model_copy()
        setting.raw_value = db_setting.raw_value
        setting.overridable = db_setting.overridable
        setting.hidden = db_setting.hidden
        setting.readonly = db_setting.readonly

        return setting

    @staticmethod
    async def get_many(
            session: AsyncSession,
            key: Optional[str] = None,
            tenant_id: Optional[str | UUID] = None,
            user_id: Optional[str | UUID] = None,
            include_none: bool = False,
    ) -> list[DbSetting]:
        """Retrieves multiple setting objects by based on the given attribute values."""
        from sqlalchemy import select

        if isinstance(tenant_id, str):
            tenant_id = UUID(tenant_id)
        if isinstance(user_id, str):
            user_id = UUID(user_id)

        stmt = select(DbSetting)

        if include_none or isinstance(key, str):
            stmt = stmt.where(DbSetting.key == key)

        if include_none or isinstance(key, str):
            stmt = stmt.where(DbSetting.key == key)

        if include_none or isinstance(tenant_id, str):
            stmt = stmt.where(DbSetting.tenant_id == tenant_id)

        if include_none or isinstance(user_id, str):
            stmt = stmt.where(DbSetting.user_id == user_id)

        return list((await session.execute(stmt)).scalars().all())

    @staticmethod
    async def create_setting(
            session: AsyncSession,
            key: str,
            value: Optional[str] = None,
            overridable: Optional[bool] = None,
            readonly: bool = False,
            tenant_id: Optional[str | UUID] = None,
            user_id: Optional[str | UUID] = None,
    ) -> DbSetting:
        """
        Creates a single setting based on the given criteria and returns the created setting object.
        """

        setting = await SettingsManager.get_by_criteria(session, key, tenant_id, user_id)

        # Validate that there isn't already an existing setting matching the given criteria
        if setting:
            raise SettingExistsException(
                f'The setting already exists: key: {key}, tenant_id: {tenant_id}, user_id: {user_id}',
                key=key,
                tenant_id=tenant_id,
                user_id=user_id,
            )

        # Validate tenant level override capability of setting if applicable
        if user_id and tenant_id:
            setting = await SettingsManager.get_by_criteria(session, key, tenant_id)
            if setting and not setting.overridable:
                raise SettingExistsException(
                    f'The setting already exists at the tenant level and cannot be overridden: '
                    + f'key: {key}, tenant_id: {tenant_id}, user_id: {user_id}',
                    key=key,
                    tenant_id=tenant_id,
                    user_id=user_id,
                )

        # Validate system level override capability of setting if applicable
        if user_id or tenant_id:
            setting = await SettingsManager.get_by_criteria(session, key, include_none=True)
            if setting and not setting.overridable:
                raise SettingExistsException(
                    f'The setting already exists at the system level and cannot be overridden: '
                    + f'key: {key}, tenant_id: {tenant_id}, user_id: {user_id}',
                    key=key,
                    tenant_id=tenant_id,
                    user_id=user_id,
                )

        setting = DbSetting(
            tenant_id=tenant_id,
            user_id=user_id,
            key=key,
            raw_value=value,
            overridable=overridable,
            readonly=readonly,
        )

        session.add(setting)
        await session.commit()
        await session.refresh(setting)

        return setting

    @staticmethod
    async def update_setting(
            session: AsyncSession,
            key: str,
            value: Optional[str] = None,
            tenant_id: Optional[str | UUID] = None,
            user_id: Optional[str | UUID] = None,
    ) -> DbSetting:
        """Updates a single setting based on the given criteria and returns the updated setting object."""

        setting = await SettingsManager.get_by_criteria(session, key, tenant_id, user_id)

        if not setting:
            raise SettingExistsException(
                f'The setting does not exist: key: {key}, tenant_id: {tenant_id}, user_id: {user_id}',
                key=key,
                tenant_id=tenant_id,
                user_id=user_id,
            )

        setting.value = value

        session.add(setting)
        await session.commit()
        await session.refresh(setting)

        return setting

    @staticmethod
    async def delete_setting(
            session: AsyncSession,
            key: str,
            tenant_id: Optional[str | UUID] = None,
            user_id: Optional[str | UUID] = None,
    ) -> None:
        """Deletes a single setting based on the given criteria and returns True if successful, False otherwise."""

        setting = await SettingsManager.get_by_criteria(session, key, tenant_id, user_id, include_none=True)

        if not setting:
            raise SettingExistsException(
                f'The setting does not exist: key: {key}, tenant_id: {tenant_id}, user_id: {user_id}',
                key=key,
                tenant_id=tenant_id,
                user_id=user_id,
            )

        await session.delete(setting)
        await session.commit()
