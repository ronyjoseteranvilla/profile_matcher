"""
    Repository layer for managing player profiles database operations.
"""

from sqlalchemy.orm import Session
from sqlalchemy import select
from web.database.models import PlayerProfile


def get_player_profiles(DB_session: Session) -> list[PlayerProfile]:
    """
    Retrieves all player profiles from the database.
    """

    query = select(PlayerProfile)
    result = DB_session.execute(query)
    return result.scalars().all()


def get_player_profile_by_id(DB_session: Session, player_id: str) -> PlayerProfile | None:
    """
    Retrieves a player profile by player ID.
    """

    query = select(PlayerProfile).where(
        PlayerProfile.player_id == player_id)
    result = DB_session.execute(query)
    return result.scalar_one_or_none()
