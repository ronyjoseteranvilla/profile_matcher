"""
    Setting up the database connection for the Profile Matcher application.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
import os

import logging
from contextlib import contextmanager, AbstractContextManager
from web.database.models import Base
from typing import Callable
logger = logging.getLogger(__name__)


class DatabaseSession:
    """
    Configuration for the database session connection.
    """

    DATABASE_PROVIDER = "postgresql+psycopg2"

    def __init__(self, database_url: str | None = None) -> None:
        """
        Initializes the database configuration.
        """

        self.USER = os.getenv("DATABASE_USER") or "your_db_user"
        self.PASSWORD = os.getenv("DATABASE_PASSWORD") or "your_db_password"
        self.HOST = os.getenv("DATABASE_HOST") or "localhost"
        self.PORT = os.getenv("DATABASE_PORT") or 5432
        self.DATABASE = os.getenv("DATABASE_NAME") or "profile_matcher_db"

        self.database_url = database_url or self.get_connection_string()

        self._engine = create_engine(self.database_url, echo=True)
        self._session = sessionmaker(bind=self._engine)

    def get_connection_string(self) -> str:
        """
        Constructs the database connection string.
        """
        return f"{self.DATABASE_PROVIDER}://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.DATABASE}"

    def create_database(self) -> None:
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
