"""
Tests for Current Campaign Service Layer
"""

from web.service import current_campaign_service
from unittest.mock import patch, Mock
import random
from utils.factories.current_campaign_factory import generate_random_current_campaign


@patch("web.repository.current_campaign_repository.get_current_campaigns")
def test_get_all_current_campaigns(get_current_campaigns_mock: Mock) -> None:
    """
    Test that all Current Campaigns are returned: Both from Database and Mocked records
    """

    # Arrange
    DB_session_mock = Mock()
    random_amount_current_campaigns = random.randint(1, 100)
    expected_database_current_campaigns = [
        generate_random_current_campaign()
        for _ in range(random_amount_current_campaigns)
    ]

    get_current_campaigns_mock.return_value = expected_database_current_campaigns

    # Act
    actual_current_campaigns = current_campaign_service.get_all_current_campaigns(
        DB_session_mock
    )

    # Assert
    assert len(actual_current_campaigns) > len(
        expected_database_current_campaigns)

    # Assert that the first records are always the ones from the DB
    assert actual_current_campaigns[:random_amount_current_campaigns] == expected_database_current_campaigns
