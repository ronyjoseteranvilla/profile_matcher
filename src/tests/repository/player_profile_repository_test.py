"""
    Tests for the PlayerProfileRepository.
"""

from web.repository import player_profile_repository
from src.web.database.connection import DatabaseSession
from utils.factories.player_profile_factory import create_and_store_player_profile


def test_get_player_profiles(DB_session: DatabaseSession):
    """
    Test retrieving all player profiles.
    """

    # Arrange
    expected_player_profiles_mock = [
        create_and_store_player_profile(
            DB_session,
        )
        for _ in range(5)
    ]

    # Act
    actual_player_profiles = player_profile_repository.get_player_profiles(
        DB_session)

    # Assert
    assert actual_player_profiles == expected_player_profiles_mock
