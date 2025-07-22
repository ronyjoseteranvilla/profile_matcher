"""
Functions to create current campaign objects for testing purposes.
"""

from web.database.connection import DatabaseSession
from web.database.models import CurrentCampaign
from utils.helpers import (generate_random_string, generate_random_int,
                           generate_random_float, generate_random_bool, generate_utc_datetime)
from typing import Final

ISO_COUNTRY_CODES: Final = ["AF", "AX", "AL", "DZ", "AS", "AD", "AO", "AI", "AQ", "AG", "AR",
                            "AM", "AW", "AU", "AT", "AZ", "BS", "BH", "BD", "BB", "BY", "BE",
                            "BZ", "BJ", "BM", "BT", "BO", "BQ", "BA", "BW", "BV", "BR", "IO",
                            "BN", "BG", "BF", "BI", "CV", "KH", "CM", "CA", "KY", "CF", "TD",
                            "CL", "CN", "CX", "CC", "CO", "KM", "CG", "CD", "CK", "CR", "CI",
                            "HR", "CU", "CW", "CY", "CZ", "DK", "DJ", "DM", "DO", "EC", "EG",
                            "SV", "GQ", "ER", "EE", "ET", "FK", "FO", "FJ", "FI", "FR", "GF",
                            "PF", "TF", "GA", "GM", "GE", "DE", "GH", "GI", "GR", "GL", "GD",
                            "GP", "GU", "GT", "GG", "GN", "GW", "GY", "HT", "HM", "VA", "HN",
                            "HK", "HU", "IS", "IN", "ID", "IR", "IQ", "IE", "IM", "IL", "IT",
                            "JM", "JP", "JE", "JO", "KZ", "KE", "KI", "KP", "KR", "KW", "KG",
                            "LA", "LV", "LB", "LS", "LR", "LY", "LI", "LT", "LU", "MO", "MK",
                            "MG", "MW", "MY", "MV", "ML", "MT", "MH", "MQ", "MR", "MU", "YT",
                            "MX", "FM", "MD", "MC", "MN", "ME", "MS", "MA", "MZ", "MM", "NA",
                            "NR", "NP", "NL", "NC", "NZ", "NI", "NE", "NG", "NU", "NF", "MP",
                            "NO", "OM", "PK", "PW", "PS", "PA", "PG", "PY", "PE", "PH", "PN",
                            "PL", "PT", "PR", "QA", "RE", "RO", "RU", "RW", "BL", "SH", "KN",
                            "LC", "MF", "PM", "VC", "WS", "SM", "ST", "SA", "SN", "RS", "SC",
                            "SL", "SG", "SX", "SK", "SI", "SB", "SO", "ZA", "GS", "SS", "ES",
                            "LK", "SD", "SR", "SJ", "SZ", "SE", "CH", "SY", "TW", "TJ", "TZ",
                            "TH", "TL", "TG", "TK", "TO", "TT", "TN", "TR", "TM", "TC", "TV",
                            "UG", "UA", "AE", "GB", "US", "UM", "UY", "UZ", "VU", "VE", "VN",
                            "VG", "VI", "WF", "EH", "YE", "ZM", "ZW"]

ITEMS_LIST = [
    "cash",
    "coins",
    "item_1",
    "item_34",
    "item_55",
    "item_312",
    "guns",
    "map"
]


def create_and_store_current_campaign(
        DB_session: DatabaseSession,
        **kwargs
) -> CurrentCampaign:
    """
    Helper function to create and store a current campaign in the database.
    """

    current_campaign = generate_random_current_campaign(**kwargs)

    DB_session.add(current_campaign)
    DB_session.commit()

    return current_campaign


def generate_random_current_campaign(**kwargs) -> CurrentCampaign:
    """
    Generate a Current Campaign with random values if they are not provided
    """

    current_campaign = CurrentCampaign(
        id=kwargs.get("id", generate_random_int()),
        name=kwargs.get("name", generate_random_string()),

        game=kwargs.get("game", generate_random_string()),
        priority=kwargs.get("priority", generate_random_float()),
        matchers=kwargs.get("matchers", {}),  # TODO: create a typedict
        enabled=kwargs.get("enabled", generate_random_bool()),

        start_date=kwargs.get("start_date", generate_random_string()),
        end_date=kwargs.get("end_date", generate_random_string()),
        last_updated=kwargs.get("last_updated", generate_random_string()),

        date_created=kwargs.get("date_created", generate_utc_datetime()),
        date_updated=kwargs.get("date_updated", generate_utc_datetime()),
        date_deleted=kwargs.get("date_deleted", generate_utc_datetime()),
    )

    return current_campaign
