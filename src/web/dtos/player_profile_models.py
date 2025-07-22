"""
DTO models representing PlayerProfile
"""

from pydantic import BaseModel, ConfigDict
from typing import Any
from datetime import datetime


class ClientConfig(BaseModel):
    """Base Model a client config (player profile)"""

    id: int
    player_id: str

    credential: str
    created: str
    modified: str
    last_session: str

    total_spent: float
    total_refund: float
    total_transactions: float
    last_purchase: str

    active_campaigns: list[str]
    devices: list[dict[Any, Any]]
    inventory: dict[Any, Any]
    clan: dict[Any, Any]

    level: int
    xp: int
    total_playtime: int
    country: str
    language: str
    birthdate: str
    gender: str

    _customfield: str

    # Additional fields for player profile
    username: str | None
    email: str | None

    # Additional fields to track when record was created, updated, or deleted
    date_created: datetime
    date_updated: datetime
    date_deleted: datetime | None

    model_config = ConfigDict(from_attributes=True)
