"""
Repository layer for managing current campaigns database operations.
"""

from sqlalchemy.orm import Session
from sqlalchemy import select
from web.database.models import CurrentCampaign


def get_current_campaigns(DB_session: Session) -> list[CurrentCampaign]:
    """
    Retrieves all current campaigns from the database
    """

    query = select(CurrentCampaign)
    result = DB_session.execute(query)

    return result.scalars().all()
