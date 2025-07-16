import pytest
from web.database.connection import DatabaseSession
import os


@pytest.fixture(scope="session")
def setup_test_database():
    """
    Fixture to provide a test database once per test session.
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
    db_session.create_database()

    return db_session


@pytest.fixture()
def DB_session(setup_test_database: DatabaseSession):
    """
    Fixture to provide a database session for each test.
    Roll back and clears the session at the end of each test.
    """

    with setup_test_database.session() as session:
        yield session
