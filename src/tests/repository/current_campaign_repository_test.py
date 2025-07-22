"""
Tests for the Current Campaign Repository Layer
"""

from web.repository import current_campaign_repository
from src.web.database.connection import DatabaseSession
from utils.factories.current_campaign_factory import create_and_store_current_campaign


def test_get_current_campaigns(DB_session: DatabaseSession) -> None:
    """
    Test retrieving all current campaigns
    """

    # Arrange
    expected_current_campaigns = [
        create_and_store_current_campaign(
            DB_session,
        )
        for _ in range(5)
    ]

    # Act
    actual_current_campaigns = current_campaign_repository.get_current_campaigns(
        DB_session
    )

    # Assert
    assert len(actual_current_campaigns) > 0
    assert actual_current_campaigns == expected_current_campaigns


def test_get_current_campaigns_with_empty_records(DB_session: DatabaseSession) -> None:
    """
    Test that returns empty list when not finding current campaigns
    """

    # Act
    actual_current_campaigns = current_campaign_repository.get_current_campaigns(
        DB_session
    )

    # Assert
    assert len(actual_current_campaigns) == 0
