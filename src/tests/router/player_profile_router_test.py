"""
Tests for calling Player Profile GET request
"""
from unittest.mock import patch, Mock
import uuid
from web.database.models import PlayerProfile
from utils.factories.player_profile_factory import generate_random_client_config
import requests
from web.repository.player_profile_repository import PlayerProfileNotFoundException


@patch("web.service.player_profile_service.get_client_config_by_id")
def test_get_client_config_by_id_success(get_client_config_by_id_mock: Mock) -> None:
    """Test that the endpoint '/get_client_config/{uuid}' gets call and returns a client configuration with 200 status"""

    # Arrange
    player_id: str = str(uuid.uuid4())
    expected_player_profile = generate_random_client_config(
        player_id=player_id)

    get_client_config_by_id_mock.return_value = expected_player_profile

    # Act
    response = requests.get(
        f"http://localhost:8080/get_client_config/{player_id}")

    # Assert
    assert response.status_code == 200
    actual_player_profile = response.json()

    assert actual_player_profile["player_id"] == expected_player_profile.player_id
    assert actual_player_profile["credential"] == expected_player_profile.credential


@patch("web.service.player_profile_service.get_client_config_by_id")
def test_get_client_config_by_id_with_exception(get_client_config_by_id_mock: Mock) -> None:
    """Test that the endpoint '/get_client_config/{uuid}' returns 404 when the player profile is not found """

    # Arrange
    player_id: str = str(uuid.uuid4())
    get_client_config_by_id_mock.side_effect = PlayerProfileNotFoundException()

    # Act
    response = requests.get(
        f"http://localhost:8080/get_client_config/{player_id}")

    # Assert
    assert response.status_code == 404
