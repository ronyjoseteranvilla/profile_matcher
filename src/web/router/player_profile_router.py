"""
    Router Layer handling API requests for the Player Profile
"""


from web.database.session import database_session_handler
from web.repository import player_profile_repository
from sqlalchemy.orm import Session
from web.database.models import PlayerProfile
import logging

logging = logging.getLogger(__name__)


@database_session_handler
def get_player_profile_by_id(DB_session: Session, player_id: str) -> dict | None:
    """Returns a single Profile Player by a given ID"""

    try:
        player_profile: None | PlayerProfile = player_profile_repository.get_player_profile_by_id(
            DB_session=DB_session, player_id=player_id)

        # TODO: raise exception when player profile is not found
        if not player_profile:
            return None

        return {
            "player_id": player_profile.player_id,
            "credential": player_profile.credential
        }
    except Exception as e:
        logging.error(
            f"Error {e} when getting a Player Profile with ID: {player_id}  ")
