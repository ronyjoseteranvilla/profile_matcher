"""
Functions to create player profile objects for testing purposes.
"""

from web.database.models import PlayerProfile
from web.database.connection import DatabaseSession

from web.dtos.player_profile_models import ClientConfig
from src.utils.helpers import (
    generate_random_string, generate_random_int, generate_random_float, generate_utc_datetime)

from uuid import uuid4


def create_and_store_player_profile(
    DB_session: DatabaseSession,
    **kwargs
) -> PlayerProfile:
    """
    Helper function to create and store a player profile in the database.
    """

    player_profile = generate_random_player_profile(**kwargs)

    DB_session.add(player_profile)
    DB_session.commit()

    return player_profile


def generate_random_player_profile(**kwargs) -> PlayerProfile:
    """
    Generate a Player Profile with random values if they are not provided
    """

    player_profile = PlayerProfile(
        player_id=kwargs.get("player_id", uuid4()),
        credential=kwargs.get("credential", generate_random_string()),
        created=kwargs.get("created", generate_random_string()),
        modified=kwargs.get("modified", generate_random_string()),
        last_session=kwargs.get("last_session", generate_random_string()),
        total_spent=kwargs.get("total_spent", generate_random_float()),
        total_refund=kwargs.get("total_refund", generate_random_float()),
        total_transactions=kwargs.get(
            "total_transactions", generate_random_float()),
        last_purchase=kwargs.get("last_purchase", generate_random_string()),
        active_campaigns=kwargs.get(
            "active_campaigns",
            [generate_random_string() for _ in range(5)]
        ),
        devices=kwargs.get("devices", [{} for _ in range(5)]),
        inventory=kwargs.get("inventory", {}),
        clan=kwargs.get("clan", {}),
        level=kwargs.get("level", generate_random_int()),
        xp=kwargs.get("xp", generate_random_int()),
        total_playtime=kwargs.get("total_playtime", generate_random_int()),
        country=kwargs.get("country", generate_random_string()),
        language=kwargs.get("language", generate_random_string()),
        birthdate=kwargs.get("birthdate", generate_random_string()),
        gender=kwargs.get("gender", generate_random_string()),

        _customfield=kwargs.get("_customfield", generate_random_string()),
        date_created=kwargs.get("date_created",  generate_utc_datetime()),
        date_updated=kwargs.get("date_updated", generate_utc_datetime()),
        date_deleted=kwargs.get("date_deleted", generate_utc_datetime()),
    )

    return player_profile


def generate_random_client_config(**kwargs) -> ClientConfig:
    """Generate a Client Config with random values if they are not set"""

    player_profile = generate_random_player_profile(**kwargs)
    client_config = ClientConfig.model_validate(player_profile)
    return client_config
