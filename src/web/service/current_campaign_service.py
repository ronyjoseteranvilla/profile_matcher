"""
Business logic for getting Current Campaign Information (Mocked and DB data)
NOTE: Instead of this service logic, I would have created a migration to ingest mock data, I'm just following the requirements of the client to create a mock service
"""

from sqlalchemy.orm import Session
from web.repository import current_campaign_repository
from web.database.models import CurrentCampaign
from utils.factories.current_campaign_factory import generate_random_current_campaign, ISO_COUNTRY_CODES, ITEMS_LIST
import random


def get_all_current_campaigns(DB_session: Session) -> list[CurrentCampaign]:
    """
    Returns a list of Current Campaigns
    - First set of items are the real database records
    - Second set of item are mock records using a factory 
    """

    current_db_campaigns = current_campaign_repository.get_current_campaigns(
        DB_session)

    current_mock_campaigns = _get_mocked_current_campaigns()

    return current_db_campaigns + current_mock_campaigns


def _get_mocked_current_campaigns() -> list[CurrentCampaign]:
    """
    Returns a list of Mock Current Campaign objects
    """

    random_amount_current_campaigns = random.randint(1, 1_000)
    mocked_current_campaigns = []

    for _ in range(random_amount_current_campaigns):
        min_level = random.randint(1, 100)
        max_level = random.randint(min_level, min_level*10)

        random_sample_of_countries = random.randint(0, len(ISO_COUNTRY_CODES))
        has_country = random.sample(
            ISO_COUNTRY_CODES,
            random_sample_of_countries
        )

        random_sample_of_items = random.randint(0, len(ITEMS_LIST))
        has_items = random.sample(
            ITEMS_LIST,
            random_sample_of_items
        )

        does_not_have_items = random.sample(
            ITEMS_LIST,
            random_sample_of_items
        )

        mocked_current_campaigns.append(
            generate_random_current_campaign(
                matchers={
                    "level": {
                        "min": min_level,
                        "max": max_level
                    },
                    "has": {
                        "country": has_country,
                        "items": has_items
                    },
                    "does_not_have": {
                        "items": does_not_have_items
                    }
                }
            )
        )

    return mocked_current_campaigns
