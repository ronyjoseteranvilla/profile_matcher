"""
Configuration file for running Tests
"""
import time
import pytest
from web.database.connection import DatabaseSession
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
import os
import threading
from app import run_serve


@pytest.fixture(scope="module", autouse=True)
def start_test_serve():
    """Run the server in a thread so it doesn't block"""

    server_thread = threading.Thread(target=run_serve, daemon=True)
    server_thread.start()
    time.sleep(1)
    yield


@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    """
    Fixture to provide a test database once per test session.
    - Creates a Database Session with the Environment variables
    - Creates the database if it doesn't exists
    - Creates the database tables
    - returns the session
    - Drops the whole database after all tests have run
    """

    db_session = DatabaseSession(
        DATABASE_USER=os.getenv("TEST_DATABASE_USER", "test"),
        DATABASE_PASSWORD=os.getenv("TEST_DATABASE_PASSWORD", "test"),
        DATABASE_HOST=os.getenv("TEST_DATABASE_HOST", "localhost"),
        DATABASE_PORT=os.getenv("TEST_DATABASE_PORT", 5433),
        DATABASE_NAME=os.getenv("TEST_DATABASE_NAME",
                                "profile_matcher_test_db"),
        DATABASE_PROVIDER=os.getenv("DATABASE_PROVIDER", "postgresql+psycopg2")
    )
    db_session.create_database_if_not_exists()
    db_session.create_database_tables()

    yield db_session

    db_session.drop_database()


@pytest.fixture(scope="function", autouse=True)
def DB_session(setup_test_database: DatabaseSession):
    """
    Fixture to provide a database session for each test.
    - Roll back and clears the session at the end of each test.
    - Removes all rows for the Database Tables
    - Closes the session
    """

    session = setup_test_database.get_session()

    yield session

    session.rollback()

    table_names = setup_test_database.get_sorted_tables_name()

    for table in table_names:
        session.execute(text(f"TRUNCATE {table} CASCADE;"))
        session.commit()

    session.close()
