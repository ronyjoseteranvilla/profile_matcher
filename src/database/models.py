"""
SqlAlchemy models for the database.
"""

from sqlalchemy import String, Integer, Float, Boolean
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from typing import List, Dict


class Base(DeclarativeBase):
    pass

class PlayerProfile(Base):
    """Represents a player's profile in the game database."""

    __tablename__ = 'player_profiles'

    id: Mapped[int] = mapped_column(primary_key=True, unique=True, autoincrement=True, nullable=False)
    player_id: Mapped[str] = mapped_column(String(30), unique=True, nullable=False )

    credential: Mapped[str] = mapped_column(String(30))
    created: Mapped[str] = mapped_column(String(30))
    modified: Mapped[str] = mapped_column(String(30))
    last_session: Mapped[str] = mapped_column(String(30))

    #Note: I added float to the following fields to match with cents for any currency
    total_spent: Mapped[float] = mapped_column()
    total_refund: Mapped[float] = mapped_column()
    total_transactions: Mapped[float] = mapped_column()
    last_purchase: Mapped[float] = mapped_column()

    
    # active_campaigns: Mapped[List[str]] = mapped_column()
    # devices: Mapped[List[Dict]] = mapped_column()
    level: Mapped[int] = mapped_column()
    xp: Mapped[int] = mapped_column()
    total_playtime: Mapped[int] = mapped_column()
    country: Mapped[str] = mapped_column(String(30))
    language: Mapped[str] = mapped_column(String(30))
    birthdate: Mapped[str] = mapped_column(String(30))
    gender: Mapped[str] = mapped_column(String(30))
    # inventory: Mapped[Dict] = mapped_column()
    # clan: Mapped[Dict] = mapped_column()
    _customfield: Mapped[str] = mapped_column(String(30), name='customfield')

    # Additional fields for player profile
    username: Mapped[str] = mapped_column(String(30))
    email: Mapped[str] = mapped_column(String(30))


    def __repr__(self):
        return f'<PlayerProfile {self.username}>'
    

class CurrentCampaign(Base):
    """Represents the current campaign for a player."""

    __tablename__ = 'current_campaigns'

    id: Mapped[int] = mapped_column(primary_key=True, unique=True, autoincrement=True, nullable=False)
    name: Mapped[str] = mapped_column(String(30))
    
    game: Mapped[str] = mapped_column(String(30))
    priority: Mapped[float] = mapped_column(String(30))
    # matchers: Mapped[Dict] = mapped_column(String(30))
    enabled: Mapped[bool] = mapped_column(String(30))

    
    start_date: Mapped[str] = mapped_column(String(30))
    end_date: Mapped[str] = mapped_column(String(30))
    last_updated: Mapped[str] = mapped_column(String(30))
    
    

    def __repr__(self):
        return f'<CurrentCampaign {self.name} for the Game {self.game}>'