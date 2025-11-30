from models.api.settings import Setting, StringSetting, IntSetting, FloatSetting, BoolSetting


class Settings:
    """Defines the available settings of the system."""

    auth_session_cookie_name: StringSetting = Setting(
        type='str',
        title='Auth Session Cookie Name',
        description='The name of the session cookie.',
        key='auth:session:cookie_name',
        default_value='session',
        overridable=False,
    )
    """Defines the name of the session cookie."""

    auth_session_expiration_age: IntSetting = Setting(
        type='int',
        title='Idle Auth Session Expiration Age',
        description='The number of seconds a session can be idle before expiring.',
        key='auth:session:expiration_age',
        default_value=3600,
        overridable=True,
    )
    """Defines the number of seconds a session can be idle before expiring."""

    auth_session_max_age: IntSetting = Setting(
        type='int',
        title='Auth Session Maximum Age',
        description='The maximum number of seconds a session can before a forced expiration.',
        key='auth:session:max_age',
        default_value=14400,
        overridable=True,
    )
    """Defines the maximum number of seconds a session can live before a forced expiration."""
