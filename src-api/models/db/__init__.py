from sqlalchemy import MetaData
from sqlalchemy.orm import declarative_base

metadata = MetaData(
    naming_convention={
        "ix": "%(column_0_label)s",
        "uq": "%(table_name)s_%(column_0_name)s",
        "ck": "%(table_name)s_%(constraint_name)s",
        "fk": "%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "%(table_name)s",
    },
)

BaseSqlModel = declarative_base(metadata=metadata)
"""This provides an abstract base class for all SQL DB app models to inherit from."""

from .acl import *
from .audits import *
from .auth import *
from .crypto import *
from .servers import *
from .system import *
from .tasks import *
from .tenants import *
from .views import *
from .zones import *
