"""
Tests for Player Profile Service Layer
"""

from utils.factories.player_profile_factory import generate_random_string, generate_random_player_profile
from utils.factories.current_campaign_factory import generate_random_current_campaign
from web.service import player_profile_service
from unittest.mock import patch, Mock
from web.dtos.player_profile_models import ClientConfig
import pytest


@patch("web.repository.player_profile_repository.update_player_profile_active_campaigns")
@patch("web.service.current_campaign_service.get_all_current_campaigns")
@patch("web.repository.player_profile_repository.get_player_profile_by_id")
def test_get_client_config_without_current_campaigns(
        get_player_profile_by_id_mock: Mock,
        get_all_current_campaigns_mock: Mock,
        update_player_profile_active_campaigns_mock: Mock) -> None:
    """
    Test that gets client config for a specific player ID
    - Gets a Player Profile by a given ID
    - When no Current Campaigns are returned we keep the same active_campaigns list from the DB
    - Returns a ClientConfig DTO
    """

    # Arrange
    DB_session_mock = Mock()
    player_id = generate_random_string()
    expected_player_profile = generate_random_player_profile(
        player_id=player_id,
    )
    expected_stored_active_campaigns = expected_player_profile.active_campaigns

    get_player_profile_by_id_mock.return_value = expected_player_profile
    get_all_current_campaigns_mock.return_value = []
    update_player_profile_active_campaigns_mock.return_value = expected_player_profile

    # Act
    actual_client_config = player_profile_service.get_client_config_by_id(
        DB_session_mock, player_id)

    # Assert
    assert isinstance(actual_client_config, ClientConfig)
    assert actual_client_config.player_id == expected_player_profile.player_id

    get_player_profile_by_id_mock.assert_called_once_with(
        DB_session_mock, player_id)
    get_all_current_campaigns_mock.assert_called_once_with(
        DB_session_mock
    )
    update_player_profile_active_campaigns_mock.assert_called_once_with(
        DB_session_mock, expected_player_profile, expected_stored_active_campaigns
    )


@patch("web.repository.player_profile_repository.update_player_profile_active_campaigns")
@patch("web.service.current_campaign_service.get_all_current_campaigns")
@patch("web.repository.player_profile_repository.get_player_profile_by_id")
def test_get_client_config_by_id_with_current_campaigns(
    get_player_profile_by_id_mock: Mock,
    get_all_current_campaigns_mock: Mock,
    update_player_profile_active_campaigns_mock: Mock
) -> None:
    """
    Test that gets client config for a specific player ID
    - Gets a Player Profile by a given ID
    - Matches the current Campaigns
    - Updates the Player Profile active campaigns
    - Returns a ClientConfig DTO
    """

    # Arrange
    DB_session_mock = Mock()
    player_id = generate_random_string()
    expected_player_profile = generate_random_player_profile(
        player_id=player_id,
        level=100,
        country="CA",
        inventory={
            "guns": 1,
            "item_09": 9,
            "item_05": 5
        }
    )

    expected_matching_current_campaigns = [
        generate_random_current_campaign(
            matchers={
                "level": {
                    "min": 50,
                    "max": 200
                },
                "has": {
                    "country": [
                        "US",
                        "CA"
                    ],
                    "items": ["guns", "item_09"]
                },
                "does_not_have": {
                    "items": [
                        "item_009"
                    ]
                }
            }
        ),
        generate_random_current_campaign(
            matchers={
                "level": {
                    "min": 100,
                    "max": 150
                },
                "has": {
                    "country": [
                        "CA"
                    ],
                    "items": ["item_05"]
                },
                "does_not_have": {
                    "items": [
                        "item_005"
                    ]
                }
            }
        )
    ]

    other_current_campaigns = [
        generate_random_current_campaign()
        for _ in range(10)
    ]

    expected_stored_active_campaigns = expected_player_profile.active_campaigns + \
        [active_campaign.name for active_campaign in expected_matching_current_campaigns]

    get_player_profile_by_id_mock.return_value = expected_player_profile
    get_all_current_campaigns_mock.return_value = other_current_campaigns + \
        expected_matching_current_campaigns
    update_player_profile_active_campaigns_mock.return_value = expected_player_profile

    # Act
    actual_client_config = player_profile_service.get_client_config_by_id(
        DB_session_mock, player_id)

    # Assert
    assert isinstance(actual_client_config, ClientConfig)
    assert actual_client_config.player_id == expected_player_profile.player_id

    get_player_profile_by_id_mock.assert_called_once_with(
        DB_session_mock, player_id)
    get_all_current_campaigns_mock.assert_called_once_with(
        DB_session_mock
    )
    update_player_profile_active_campaigns_mock.assert_called_once_with(
        DB_session_mock, expected_player_profile, expected_stored_active_campaigns
    )


@pytest.mark.parametrize(
    "player_level,min_level,max_level,expected_is_matching_level",
    [
        (2, 1, 3, True),
        (10, 11, 12, False),
        (10_000, 10_000, 30_000, True),
        (30, 25, 30, True),
        (30, 25, 29, False),
    ]
)
def test_is_matching_level(player_level: int, min_level: int, max_level: int, expected_is_matching_level: bool) -> None:
    """
    Test that checks if a Player Profile Level is matching the level range of the Current Campaign
    """

    # Arrange
    player_profile = generate_random_player_profile(
        level=player_level,
    )
    current_campaign = generate_random_current_campaign(
        matchers={
            "level": {
                "min": min_level,
                "max": max_level
            },
        }
    )

    # Act
    actual_is_matching_level = player_profile_service.is_matching_level(
        player_profile, current_campaign)

    # Assert
    assert actual_is_matching_level is expected_is_matching_level


def test_is_matching_level_when_matchers_are_not_set() -> None:
    """
    Test that function returns False, when Current Campaign has No Matchers Data
    """

    # Arrange
    player_profile = generate_random_player_profile(
        level=5,
    )

    current_campaign = generate_random_current_campaign(
        matchers={}
    )

    # Act
    actual_is_matching_level = player_profile_service.is_matching_level(
        player_profile, current_campaign)

    # Assert
    assert actual_is_matching_level is False


@pytest.mark.parametrize(
    "player_country,country_matcher,player_item,item_matcher,expected_is_matching_has_country_and_items",
    [
        ("RO", ["US", "MX", "RO"], "item_1", ["item_1"], True),
        ("VZ", ["US", "RO", "vz"],
         "item_0005", ["item_0005", "item_09", "ITEM_1"], True),
        ("MX", ["US", "PO", "VZ"], "item_01", ["item_01"], False)
    ]
)
def test_is_matching_has_country_and_items(
    player_country: str, country_matcher: list[str], player_item: str, item_matcher: list[str], expected_is_matching_has_country_and_items: bool
) -> None:
    """
    Tests that checks if a Player Profile data matches a Current Campaign 'has' key
    - Check if Player Profile Country is inside the list of Countries for the Current Campaign
    - Check if Player Profile Inventory key name exists inside the list of Items for the Current Campaign
    """

    # Arrange
    player_profile = generate_random_player_profile(
        country=player_country,
        inventory={
            "cash": 123,
            "coins": 123,
            player_item: 1,
            "item_34": 3,
            "item_55": 2
        }
    )
    current_campaign = generate_random_current_campaign(
        matchers={
            "has": {
                "country": country_matcher,
                "items": item_matcher
            }
        }
    )

    # Act
    actual_is_matching_has_country_and_items = player_profile_service.is_matching_has_country_and_items(
        player_profile, current_campaign
    )

    # Assert
    assert actual_is_matching_has_country_and_items is expected_is_matching_has_country_and_items


def test_is_matching_does_not_have_items_with_true_response() -> None:
    """
    Tests that method returns True if the Player Profile has the items from Current Campaign 'does_not_have' matcher key 
    """

    # Arrange
    player_profile = generate_random_player_profile(
        inventory={
            "cash": 456
        }
    )
    current_campaign = generate_random_current_campaign(
        matchers={
            "does_not_have": {
                "items": [
                    "cash"
                ]
            }
        }
    )

    # Act
    actual_is_matching_does_not_have_items = player_profile_service.is_matching_does_not_have_items(
        player_profile, current_campaign
    )

    # Assert
    assert actual_is_matching_does_not_have_items is True


def test_is_matching_does_not_have_items_with_false_response() -> None:
    """
    Tests that method returns False if the Player Profile does not have the items from Current Campaign 'does_not_have' matcher key
    """

    # Arrange
    player_profile = generate_random_player_profile(
        inventory={
            "cash": 456,
            "item_02": 55
        }
    )
    current_campaign = generate_random_current_campaign(
        matchers={
            "does_not_have": {
                "items": [
                    "item_01",
                    "item_03"
                ]
            }
        }
    )

    # Act
    actual_is_matching_does_not_have_items = player_profile_service.is_matching_does_not_have_items(
        player_profile, current_campaign
    )

    # Assert
    assert actual_is_matching_does_not_have_items is False
