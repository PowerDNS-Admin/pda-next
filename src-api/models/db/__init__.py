from sqlalchemy import MetaData
from sqlalchemy.orm import declarative_base
from sqlalchemy.types import TypeDecorator, TEXT

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


class JSONType(TypeDecorator):
    """Stores JSON data as TEXT in the database, automatically encoding on the way in and decoding on the way out."""
    impl = TEXT  # The underlying column data type

    def process_bind_param(self, value, dialect):
        """Called when saving data to the database (Python -> DB)."""
        import json
        if value is not None:
            return json.dumps(value)
        return None

    def process_result_value(self, value, dialect):
        """Called when loading data from the database (DB -> Python)."""
        import json
        if value is not None:
            return json.loads(value)
        return None


from .acl import *
from .audits import *
from .auth import *
from .keys import *
from .servers import *
from .settings import *
from .system import *
from .tasks import *
from .tenants import *
from .views import *
from .zones import *
