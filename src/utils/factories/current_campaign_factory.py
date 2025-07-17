"""
Functions to create current campaign objects for testing purposes.
"""

from web.database.connection import DatabaseSession
from web.database.models import CurrentCampaign
from src.utils.helpers import (generate_random_string, generate_random_int,
                               generate_random_float, generate_random_bool, generate_utc_datetime)


def create_and_store_current_campaign(
        DB_session: DatabaseSession,
        **kwargs
) -> CurrentCampaign:
    """
    Helper function to create and store a current campaign in the database.
    """

    current_campaign = generate_random_current_campaign(**kwargs)

    DB_session.add(current_campaign)
    DB_session.commit()

    return current_campaign


def generate_random_current_campaign(**kwargs) -> CurrentCampaign:
    """
    Generate a Current Campaign with random values if they are not provided
    """

    current_campaign = CurrentCampaign(
        id=kwargs.get("id", generate_random_int()),
        name=kwargs.get("name", generate_random_string()),

        game=kwargs.get("game", generate_random_string()),
        priority=kwargs.get("priority", generate_random_float()),
        matchers=kwargs.get("matchers", {}),  # TODO: create a typedict
        enabled=kwargs.get("enabled", generate_random_bool()),

        start_date=kwargs.get("start_date", generate_random_string()),
        end_date=kwargs.get("end_date", generate_random_string()),
        last_updated=kwargs.get("last_updated", generate_random_string()),

        date_created=kwargs.get("date_created", generate_utc_datetime()),
        date_updated=kwargs.get("date_updated", generate_utc_datetime()),
        date_deleted=kwargs.get("date_deleted", generate_utc_datetime()),
    )

    return current_campaign
