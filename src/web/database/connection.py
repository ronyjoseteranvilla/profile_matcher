"""
Setting up the database connection for the Profile Matcher application.
"""
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

import logging
from contextlib import contextmanager, AbstractContextManager
from web.database.models import Base
from typing import Callable


logger = logging.getLogger(__name__)


class DatabaseSession:
    """
    Configuration for the database session connection.
    """

    def __init__(
            self,
            **kwargs: str,
    ) -> None:
        """
        Initializes the database configuration.
        """

        self.USER = kwargs.get("DATABASE_USER", "your_db_user")
        self.PASSWORD = kwargs.get("DATABASE_PASSWORD", "your_db_password")
        self.HOST = kwargs.get("DATABASE_HOST", "localhost")
        self.PORT = kwargs.get("DATABASE_PORT", 5432)
        self.DATABASE = kwargs.get("DATABASE_NAME", "profile_matcher_db")
        self.DATABASE_PROVIDER = kwargs.get(
            "DATABASE_PROVIDER", "db_provider:provider_package")

        self.database_url = self.get_connection_string()

        self._engine = create_engine(self.database_url, echo=True)
        self._session = sessionmaker(bind=self._engine, expire_on_commit=False)

    def get_connection_string(self) -> str:
        """
        Constructs the database connection string.
        """
        return f"{self.DATABASE_PROVIDER}://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.DATABASE}"

    def create_database_if_not_exists(self) -> None:
        """
        Checks if the database exists, and creates it if it does not.
        """
        logger.info(f"Checking if database {self.DATABASE} exists...")

        if not database_exists(self._engine.url):
            create_database(self._engine.url)
            logger.info(f"Database {self.DATABASE} created.")
        else:
            logger.info(f"Database {self.DATABASE} already exists.")

    def create_database_tables(self) -> None:
        Base.metadata.create_all(self._engine)

    @contextmanager
    def session(self) -> Callable[..., AbstractContextManager[Session]]:
        """
        Context manager for creating a new session.
        """
        session: Session = self._session()
        try:
            yield session
            session.commit()
        except Exception as e:
            logger.error(f"Error: {e} - Rolling back session.")
            session.rollback()
            raise
        finally:
            session.close()

    def get_session(self) -> Session:
        return self._session()

    def drop_database(self) -> None:
        """
        Removes all Tables from the Database
        """

        logger.info(f"Removing Tables from DB: {self.DATABASE}")

        metadata = Base.metadata
        metadata.reflect(bind=self._engine)
        metadata.drop_all(self._engine)

        self.session()

    def get_sorted_tables_name(self) -> list[str]:
        """
        Return a reversed sorted list of Table names
        """

        logger.info(f"Returning Sorted Tables")

        metadata = Base.metadata
        tables = reversed(metadata.sorted_tables)

        return [
            table.name
            for table in tables
        ]
