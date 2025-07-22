"""
Router Layer handling API requests for the Player Profile
"""


from web.database.session import database_session_handler
from sqlalchemy.orm import Session
from web.dtos.player_profile_models import ClientConfig
import logging
from web.service import player_profile_service

from uuid import UUID

logging = logging.getLogger(__name__)


@database_session_handler
def get_client_config_by_id(DB_session: Session, player_id: UUID) -> ClientConfig:
    """Returns a single Profile Player by a given ID"""

    client_config = player_profile_service.get_client_config_by_id(
        DB_session=DB_session, player_id=player_id)

    return client_config
