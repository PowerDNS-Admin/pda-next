from pydantic import BaseModel

from lib.settings import Setting
from models.enums import SettingTypeEnum


class Settings(BaseModel):
    """Defines the available settings of the system."""

    auth_session_cookie_name: Setting = Setting(
        title='Auth Session Cookie Name',
        description='The name of the session cookie.',
        key='auth:session:cookie_name',
        data_type=SettingTypeEnum.str,
        default_value='session',
        overridable=False,
        hidden=True,
    )
    """Defines the name of the session cookie."""

    auth_session_expiration_age: Setting = Setting(
        title='Idle Auth Session Expiration Age',
        description='The number of seconds a session can be idle before expiring.',
        key='auth:session:expiration_age',
        data_type=SettingTypeEnum.int,
        default_value=3600,
        overridable=True,
    )
    """Defines the number of seconds a session can be idle before expiring."""

    auth_session_max_age: Setting = Setting(
        title='Auth Session Maximum Age',
        description='The maximum number of seconds a session can before a forced expiration.',
        key='auth:session:max_age',
        data_type=SettingTypeEnum.int,
        default_value=14400,
        overridable=True,
    )
    """Defines the maximum number of seconds a session can live before a forced expiration."""

    auth_access_token_age: Setting = Setting(
        title='Auth Access Token Age',
        description='The maximum number of seconds an OAuth access token is good for.',
        key='auth:access_token:age',
        data_type=SettingTypeEnum.int,
        default_value=3600,
        overridable=True,
    )
    """Defines the maximum number of seconds an OAuth access token is good for."""

    auth_refresh_token_age: Setting = Setting(
        title='Auth Refresh Token Age',
        description='The maximum number of seconds an OAuth refresh token is good for.',
        key='auth:refresh_token:age',
        data_type=SettingTypeEnum.int,
        default_value=1800,
        overridable=True,
    )
    """Defines the maximum number of seconds an OAuth refresh token is good for."""


sd: Settings = Settings()
sdk: dict[str, Setting] = {s.key: s for s in list(dict(sd).values())}
