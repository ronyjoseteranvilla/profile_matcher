"""
SqlAlchemy models for the database.
"""


from datetime import datetime, timezone
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.types import JSON
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import JSON as PostJson, ARRAY as PostArray


class Base(AsyncAttrs, DeclarativeBase):

    type_annotation_map = {
        PostJson: JSON,
        PostArray: JSON
    }


class PlayerProfile(Base):
    """Represents a player's profile in the game database."""

    __tablename__ = 'player_profiles'

    id: Mapped[int] = mapped_column(
        primary_key=True, unique=True, autoincrement=True, nullable=False)
    player_id: Mapped[str] = mapped_column(
        unique=True, nullable=False)  # TODO: Move this to UUID

    credential: Mapped[str]
    created: Mapped[str]
    modified: Mapped[str]
    last_session: Mapped[str]

    # Note: I added float to the following fields to match with cents for any currency
    total_spent: Mapped[float]
    total_refund: Mapped[float]
    total_transactions: Mapped[float]
    last_purchase: Mapped[str]

    # TODO: change to relationship with CurrentCampaign
    active_campaigns: Mapped[PostArray[str]]
    devices: Mapped[PostArray[PostJson]]
    level: Mapped[int]
    xp: Mapped[int]
    total_playtime: Mapped[int]
    country: Mapped[str]
    language: Mapped[str]
    birthdate: Mapped[str]
    gender: Mapped[str]
    inventory: Mapped[PostJson]
    clan: Mapped[PostJson]
    _customfield: Mapped[str]

    # Additional fields for player profile
    username: Mapped[str | None]
    email: Mapped[str | None]

    # Additional fields to track when record was created, updated, or deleted
    date_created: Mapped[datetime] = mapped_column(
        default=datetime.now(timezone.utc), server_default=func.now())
    date_updated: Mapped[datetime] = mapped_column(
        default=datetime.now(timezone.utc), server_default=func.now())
    date_deleted: Mapped[datetime] = mapped_column(default=None, nullable=True)

    def __repr__(self):
        return f'<PlayerProfile {self.username}>'


class CurrentCampaign(Base):
    """Represents the current campaign for a player."""

    __tablename__ = 'current_campaigns'

    id: Mapped[int] = mapped_column(
        primary_key=True, unique=True, autoincrement=True, nullable=False)
    name: Mapped[str]

    game: Mapped[str]
    priority: Mapped[float]
    matchers: Mapped[PostJson]
    enabled: Mapped[bool]

    start_date: Mapped[str]
    end_date: Mapped[str]
    last_updated: Mapped[str]

    # Additional fields to track when record was created, updated, or deleted
    date_created: Mapped[datetime] = mapped_column(
        default=datetime.now(timezone.utc), server_default=func.now())
    date_updated: Mapped[datetime] = mapped_column(
        default=datetime.now(timezone.utc), server_default=func.now())
    date_deleted: Mapped[datetime] = mapped_column(default=None, nullable=True)

    def __repr__(self):
        return f'<CurrentCampaign {self.name} for the Game {self.game}>'
