"""
Database connection scripts
"""

from web.database.connection import DatabaseSession
from sqlalchemy.orm import Session
from functools import wraps
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

    database_session = init_database_session()

    return database_session.get_session()


def database_session_handler(func):
    """
    Decorator to inject a session into the function.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        session = get_database_session()

        try:
            result = func(session, *args, **kwargs)
            session.commit()
            return result
        except Exception as e:
            session.rollback()
            logging.error(f"Error with Database session: {e}")
            raise
        finally:
            session.close()

    return wrapper
