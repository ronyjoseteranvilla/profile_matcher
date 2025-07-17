"""
Tests for the Player Profile Repository Layer.
"""
import pytest
from web.repository import player_profile_repository
from src.web.database.connection import DatabaseSession
from utils.factories.player_profile_factory import create_and_store_player_profile
import uuid


def test_get_player_profiles(DB_session: DatabaseSession) -> None:
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


def test_get_player_profile_by_id_with_success(DB_session: DatabaseSession) -> None:
    """
    Test retrieving a single player by ID succeeds 
    """

    # Arrange
    expected_player_id = str(uuid.uuid4())
    expected_player_profile = create_and_store_player_profile(
        DB_session, player_id=expected_player_id)

    _ = create_and_store_player_profile(
        DB_session
    )

    # Act
    actual_player_profile = player_profile_repository.get_player_profile_by_id(
        DB_session, expected_player_id)

    # Assert
    assert actual_player_profile.player_id == expected_player_id
    assert actual_player_profile == expected_player_profile


def test_get_player_profile_by_id_with_exception(DB_session: DatabaseSession) -> None:
    """
    Test that PlayerProfileNotFoundException is raised when the player profile is not found
    """

    # Arrange
    player_id = str(uuid.uuid4())
    _ = create_and_store_player_profile(DB_session)

    # Act | Assert
    with pytest.raises(player_profile_repository.PlayerProfileNotFoundException):
        _ = player_profile_repository.get_player_profile_by_id(
            DB_session, player_id)
