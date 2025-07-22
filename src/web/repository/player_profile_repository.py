"""
Repository layer for managing player profiles database operations.
"""

from sqlalchemy.orm import Session
from sqlalchemy import select
from web.database.models import PlayerProfile
from uuid import UUID


class PlayerProfileNotFoundException(Exception):
    """Raised when a Player Profile is not found by a given ID"""

    def __init__(self, message: str = "Player Profile Not Found"):
        self.message = message
        super().__init__(message)


def get_player_profiles(DB_session: Session) -> list[PlayerProfile]:
    """
    Retrieves all player profiles from the database.
    """

    query = select(PlayerProfile)
    result = DB_session.execute(query)
    return result.scalars().all()


def get_player_profile_by_id(DB_session: Session, player_id: UUID) -> PlayerProfile:
    """
    Retrieves a player profile by player ID.
    """

    query = select(PlayerProfile).where(
        PlayerProfile.player_id == player_id)
    result = DB_session.execute(query)

    player_profile = result.scalar_one_or_none()

    if not player_profile:
        raise PlayerProfileNotFoundException(
            message=f"The Player Profile with ID: {player_id} was not found")

    return player_profile


def update_player_profile_active_campaigns(DB_session: Session, player_profile: PlayerProfile, active_campaigns: list[str]) -> PlayerProfile:
    """
    Updates a Player Profile Active Campaigns column
    """

    DB_session.query(PlayerProfile).filter(
        PlayerProfile.player_id == player_profile.player_id).update({"active_campaigns": active_campaigns})
    DB_session.commit()

    return player_profile
