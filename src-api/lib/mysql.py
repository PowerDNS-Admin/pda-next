from sqlalchemy import create_engine, Connection, Engine
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncEngine, AsyncConnection, AsyncSession
from sqlalchemy.orm import Session
from typing import Union
from lib.config.db import MySQLDatabaseConnection
from models import BaseModel
from models.db import BaseSqlModel


class MysqlDbConfig(BaseModel):
    """This model defines a database connection configuration for accessing the central PDA MySQL database."""
    host: str
    port: int
    username: str
    password: str
    database: str


class MysqlClient:
    """This class provides a simple API for instantiating MySQL server connections."""

    _config: Union[MySQLDatabaseConnection, MysqlDbConfig]
    """The Mysql configuration object."""

    _engine: Engine = None
    """The Mysql engine object."""

    _connection: Connection = None
    """The Mysql connection object."""

    _session: Session = None
    """The Mysql session object."""

    @property
    def config(self) -> MysqlDbConfig:
        """The MySQL connection configuration object."""
        return self._config

    @property
    def engine(self) -> Engine:
        """The MySQL engine object."""
        return self._engine

    @property
    def connection(self) -> Connection:
        """The MySQL connection object."""
        return self._connection

    def __init__(self, config: Union[MySQLDatabaseConnection, MysqlDbConfig], auto_connect: bool = True, **kwargs):
        self._config = config

        # Set up the Mysql connection
        self.setup(**kwargs)

        # Initiate auto-connect for Mysql if set accordingly
        if auto_connect:
            self.connect()

    def __enter__(self) -> Session:
        """Create a new MySQL session with the current engine."""
        with Session(self._engine) as session:
            self._session = session
            return session

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Close the current MySQL session."""
        self._session.close()

    def setup(self, **kwargs):
        """Set up the Mysql engine."""
        conn_str = (f'mysql+pymysql://{self._config.username}:{self._config.password}@{self._config.host}'
                    + f':{self._config.port}/{self._config.database}')
        self._engine = create_engine(conn_str, **kwargs)

    def connect(self):
        """Create a connection to the Mysql database."""
        if self._engine is None:
            self.setup()
        self._connection = self._engine.connect()

    def disconnect(self):
        """Disconnect the current connection."""
        if self._connection is None or self._connection.closed:
            return
        self._connection.close()

    def create_schema(self):
        """Creates the associated database schema."""
        from loguru import logger

        logger.debug(f'Creating MySQL database tables: {", ".join(BaseSqlModel.metadata.tables.keys())}')

        BaseSqlModel.metadata.create_all(self.engine)

        logger.debug('MySQL database schema updated!')


class MysqlAsyncClient:
    """This class provides a simple API for instantiating MySQL server asynchronous connections."""

    _config: Union[MySQLDatabaseConnection, MysqlDbConfig]
    """The Mysql configuration object."""

    _engine: AsyncEngine = None
    """The Mysql engine object."""

    _connection: AsyncConnection = None
    """The Mysql connection object."""

    _session_maker: async_sessionmaker[AsyncSession] = None
    """The MySQL session maker factory."""

    _session: AsyncSession = None
    """The Mysql session object."""

    @property
    def config(self) -> MysqlDbConfig:
        """The MySQL connection configuration object."""
        return self._config

    @property
    def engine(self) -> AsyncEngine:
        """The MySQL engine object."""
        return self._engine

    @property
    def connection(self) -> AsyncConnection:
        """The MySQL connection object."""
        return self._connection

    @property
    def session_maker(self) -> async_sessionmaker[AsyncSession]:
        """The Mysql session maker factory."""
        return self._session_maker

    def __init__(self, config: Union[MySQLDatabaseConnection, MysqlDbConfig], **kwargs):
        self._config = config

        # Set up the Mysql connection
        self.setup(**kwargs)

    async def __aenter__(self) -> AsyncSession:
        """Create a new MySQL session with the current engine."""
        async with self._session_maker() as session:
            self._session = session
            return session

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Close the current MySQL session."""
        await self._session.close()

    def setup(self, **kwargs):
        """Set up the Mysql engine."""
        conn_str = (f'mysql+asyncmy://{self._config.username}:{self._config.password}@{self._config.host}'
                    + f':{self._config.port}/{self._config.database}')
        self._engine = create_async_engine(conn_str, **kwargs)
        self._session_maker = async_sessionmaker(self.engine, expire_on_commit=False)

    async def connect(self):
        """Create a connection to the Mysql database."""
        if self._engine is None:
            self.setup()
        self._connection = await self._engine.connect()

    async def disconnect(self):
        """Disconnect the current connection."""
        if self._connection is None or self._connection.closed:
            return
        await self._connection.close()

    async def create_schema(self):
        """Creates the associated database schema."""
        from loguru import logger

        logger.debug(f'Creating MySQL database tables: {", ".join(BaseSqlModel.metadata.tables.keys())}')

        async with self.engine.begin() as conn:
            await conn.run_sync(BaseSqlModel.metadata.create_all)

        logger.debug('MySQL database schema updated!')
