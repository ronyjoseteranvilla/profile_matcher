"""
Tests for Player Profile Service Layer
"""


import pytest
from utils.factories.player_profile_factory import generate_random_string, generate_random_player_profile
from web.service import player_profile_service
from unittest.mock import patch, Mock
from web.database.models import PlayerProfile
from web.dtos.player_profile_models import ClientConfig


@patch("web.repository.player_profile_repository.get_player_profile_by_id")
def test_get_client_config(get_player_profile_by_id_mock: Mock) -> None:
    """
    Test that gets client config for a specific player ID
    """

    # Arrange
    DB_session_mock = Mock()
    player_id = generate_random_string()
    expected_player_profile: PlayerProfile = generate_random_player_profile(
        player_id=player_id
    )

    get_player_profile_by_id_mock.return_value = expected_player_profile

    # Act
    actual_client_config = player_profile_service.get_client_config(
        DB_session_mock, player_id)

    # Assert
    assert isinstance(actual_client_config, ClientConfig)
    assert actual_client_config.player_id == expected_player_profile.player_id
