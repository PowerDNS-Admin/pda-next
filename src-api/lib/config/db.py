from typing import Optional, Union
from models import BaseConfig


class DatabaseConnection(BaseConfig):
    host: str = 'localhost'
    port: int = 0
    username: Union[str, None] = None
    password: Union[str, None] = None
    database: Union[str, None] = None


class MySQLDatabaseConnection(DatabaseConnection):
    port: int = 3306


class RedisDatabaseConnection(DatabaseConnection):
    host: str = 'redis'
    port: int = 6379
    database: Union[int, str, None] = 0


class DbConfig(BaseConfig):
    """A model that represents a configuration hierarchy for database connection settings."""
    mysql: MySQLDatabaseConnection
    redis: RedisDatabaseConnection
    sql_url: Optional[str] = 'sqlite+aiosqlite:///./pda.db'
