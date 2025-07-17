"""
    Router Layer handling API requests for the Player Profile
"""


from web.database.session import database_session_handler
from sqlalchemy.orm import Session
from web.dtos.player_profile_models import ClientConfig
import logging
from web.service import player_profile_service

logging = logging.getLogger(__name__)


@database_session_handler
def get_client_config_by_id(DB_session: Session, player_id: str) -> ClientConfig | None:
    """Returns a single Profile Player by a given ID"""

    try:
        client_config: ClientConfig | None = player_profile_service.get_client_config_by_id(
            DB_session=DB_session, player_id=player_id)

        # TODO: raise exception when player profile is not found
        if not client_config:
            return None

        return client_config
    except Exception as e:
        logging.error(
            f"Error {e} when getting a Player Profile with ID: {player_id}  ")
