"""

"""

from web.database.connection import DatabaseSession
from sqlalchemy.orm import Session

import logging

import os
from typing import Optional


logger = logging.getLogger(__name__)

_db_instance: Optional[DatabaseSession] = None


def init_database_session() -> DatabaseSession:
    """Initiate a database session instance if there is None"""

    global _db_instance
    if _db_instance is None:
        _db_instance = DatabaseSession(
            DATABASE_USER=os.getenv("DATABASE_USER", "your_db_user"),
            DATABASE_PASSWORD=os.getenv(
                "DATABASE_PASSWORD", "your_db_password"),
            DATABASE_HOST=os.getenv("DATABASE_HOST", "localhost"),
            DATABASE_PORT=os.getenv("DATABASE_PORT", 5432),
            DATABASE_NAME=os.getenv("DATABASE_NAME", "profile_matcher_db"),
            DATABASE_PROVIDER=os.getenv(
                "DATABASE_PROVIDER", "postgresql+psycopg2")
        )

    return _db_instance


def get_database_session() -> Session:
    """Get database session to be used in the repository layer"""

    # TODO: fix this
    database = init_database_session()
    return database.get_session()

    # try:
    #     yield session  # when used in a fixture
    # except Exception as e:
    #     session.rollback()
    #     logger.error(f"Session error: {e}")
    #     raise
    # else:
    #     session.commit()
    # finally:
    #     session.close()
