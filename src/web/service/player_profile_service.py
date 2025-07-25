"""
Business logic for getting a Client Configuration (Player Profile)
"""

from sqlalchemy.orm import Session
from web.dtos.player_profile_models import ClientConfig
from web.repository import player_profile_repository
from web.database.models import PlayerProfile, CurrentCampaign
from web.service import current_campaign_service
from uuid import UUID


def get_client_config_by_id(DB_session: Session, player_id: UUID) -> ClientConfig:
    """
        Get Client Config (Player Profile) by a given player_id

        - Gets Player Profile
        - Gets Current Campaigns
        - Match Player Profile details with Current Campaigns also checks that the campaign name is not already stored
        - Add Matched Current Campaigns to the Player Profile
        - Return Client Config
    """

    player_profile = player_profile_repository.get_player_profile_by_id(
        DB_session, player_id)

    current_campaigns = current_campaign_service.get_all_current_campaigns(
        DB_session)
    player_profile_active_campaigns = player_profile.active_campaigns

    for current_campaign in current_campaigns:
        if (
            is_matching_with_current_campaign(
                player_profile, current_campaign
            )
            and
            current_campaign.name not in player_profile_active_campaigns
        ):
            player_profile_active_campaigns.append(current_campaign.name)

    player_profile = player_profile_repository.update_player_profile_active_campaigns(
        DB_session, player_profile, player_profile_active_campaigns
    )

    client_config = ClientConfig.model_validate(player_profile)
    return client_config


def is_matching_with_current_campaign(player_profile: PlayerProfile, current_campaign: CurrentCampaign) -> bool:
    """
    Checks if Player Profile data matches with the Current Campaign
    """

    return (
        is_matching_level(player_profile, current_campaign) and
        is_matching_has_country_and_items(player_profile, current_campaign) and
        not is_matching_does_not_have_items(player_profile, current_campaign)
    )


def is_matching_level(player_profile: PlayerProfile, current_campaign: CurrentCampaign) -> bool:
    """
    Checks if the PlayerProfile level is between the Min and Max for the CurrentCampaign level Matcher
    """

    if not current_campaign.matchers.get("level", {}).get("min") and not current_campaign.matchers.get("level", {}).get("max"):
        return False

    return current_campaign.matchers["level"]["min"] <= player_profile.level <= current_campaign.matchers["level"]["max"]


def is_matching_has_country_and_items(player_profile: PlayerProfile, current_campaign: CurrentCampaign) -> bool:
    """
    Checks if PlayerProfile country is inside the CurrentCampaign country has Matcher
    - Transform all Country str into lowercase, to prevent matching errors
    - Items should be match as they are.
    """

    if (
        not current_campaign.matchers.get("has", {}).get("country") or
        not current_campaign.matchers.get("has", {}).get("items")
    ):
        return False

    current_campaign_countries = [
        country.lower()
        for country in current_campaign.matchers["has"]["country"]
    ]

    return player_profile.country.lower() in current_campaign_countries and any([
        player_profile.inventory.get(item, False)
        for item in current_campaign.matchers["has"]["items"]
    ])


def is_matching_does_not_have_items(player_profile: PlayerProfile, current_campaign: CurrentCampaign) -> bool:
    """
    Checks if Player Profile does not have the items from the Current Campaign
    - Return True if the Player Profile has the item
    - Return False if the Player Profile does not have the item
    """
    if not current_campaign.matchers.get("does_not_have", {}).get("items"):
        return False

    return any([
        player_profile.inventory.get(item, False)
        for item in current_campaign.matchers["does_not_have"]["items"]
    ])
