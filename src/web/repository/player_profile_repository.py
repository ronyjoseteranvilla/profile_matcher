"""
    Repository layer for managing player profiles database operations.
"""

from web.database.connection import DatabaseSession
from web.database.session import get_database_session

from sqlalchemy import select
from web.database.models import PlayerProfile


def get_player_profiles(DB_session: DatabaseSession) -> list[PlayerProfile]:
    """
    Retrieves all player profiles from the database.
    """

    # with DB_session.session() as db_session:
    #     query = select(PlayerProfile)
    #     result = db_session.execute(query)
    #     return result.scalars().all()

    # TODO: Fix session, Fixture works on test but not when running the script
    query = select(PlayerProfile)
    result = DB_session.execute(query)
    return result.scalars().all()


def get_player_profile_by_id(DB_session: DatabaseSession, player_id: str) -> PlayerProfile | None:
    """
    Retrieves a player profile by player ID.
    """

    with DB_session.session() as db_session:
        query = select(PlayerProfile).where(
            PlayerProfile.player_id == player_id)
        result = db_session.execute(query)
        return result.scalar_one_or_none()


if __name__ == "__main__":
    # Example usage
    profiles = get_player_profiles(DB_session=get_database_session())
    print(f"Retrieved {len(profiles)} player profiles:")
    for profile in profiles:
        print(profile)
