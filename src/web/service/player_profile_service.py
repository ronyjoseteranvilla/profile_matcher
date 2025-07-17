"""
Business logic for getting a Client Configuration (Player Profile)
"""

from sqlalchemy.orm import Session
from web.dtos.player_profile_models import ClientConfig
from web.repository import player_profile_repository
from web.database.models import CurrentCampaign


def get_client_config_by_id(DB_session: Session, player_id: str) -> ClientConfig:
    """
        Get Client Config (Player Profile) by a given player_id

        - Gets Player Profile
        - Gets Current Campaigns
        - Match Player Profile details with Current Campaigns
        - Add Matched Current Campaigns to the Player Profile
        - Return Client Config
    """

    player_profile = player_profile_repository.get_player_profile_by_id(
        DB_session, player_id)

    current_campaigns: list[CurrentCampaign] = [

    ]

    # Match player profile with current campaign

    # Update player profile

    # return client config
    client_config = ClientConfig.model_validate(player_profile)
    return client_config
