"""
    Functions to create player profile objects for testing purposes.
"""
import random
import string
from web.database.models import PlayerProfile
from web.database.connection import DatabaseSession
from datetime import datetime, timezone


def generate_random_string(length: int = 10) -> str:
    """
    Generates a random string of fixed length.
    """

    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(length))


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
    """Generate a Player Profile with random values if they are not set"""

    player_profile = PlayerProfile(
        id=kwargs.get("id", random.randint(1, 1_000)),
        player_id=kwargs.get("player_id", generate_random_string()),
        credential=kwargs.get("credential", generate_random_string()),
        created=kwargs.get("created", generate_random_string()),
        modified=kwargs.get("modified", generate_random_string()),
        last_session=kwargs.get("last_session", generate_random_string()),
        total_spent=kwargs.get("total_spent", random.random()),
        total_refund=kwargs.get("total_refund", random.random()),
        total_transactions=kwargs.get(
            "total_transactions", random.random()),
        last_purchase=kwargs.get("last_purchase", generate_random_string()),
        active_campaigns=kwargs.get(
            "active_campaigns",
            [generate_random_string() for _ in range(5)]
        ),
        devices=kwargs.get("devices", [{} for _ in range(5)]),
        inventory=kwargs.get("inventory", {}),
        clan=kwargs.get("clan", {}),
        level=kwargs.get("level", random.randint(1, 1_000)),
        xp=kwargs.get("xp", random.randint(1, 1_000)),
        total_playtime=kwargs.get("total_playtime", random.randint(1, 1_000)),
        country=kwargs.get("country", generate_random_string()),
        language=kwargs.get("language", generate_random_string()),
        birthdate=kwargs.get("birthdate", generate_random_string()),
        gender=kwargs.get("gender", generate_random_string()),

        _customfield=kwargs.get("_customfield", generate_random_string()),
        date_created=kwargs.get("date_created",  datetime.now(timezone.utc)),
        date_updated=kwargs.get("date_updated", datetime.now(timezone.utc)),
        date_deleted=kwargs.get("date_deleted", datetime.now(timezone.utc)),
    )

    return player_profile
