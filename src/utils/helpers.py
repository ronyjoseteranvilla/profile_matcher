"""
Helper Functions for setting up tests.
"""
from datetime import datetime, timezone
import random
import string


def generate_random_string(length: int = 10) -> str:
    """
    Generates a random string of fixed length.
    """

    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(length))


def generate_random_int() -> int:
    """
    Generates a random int of fixed length.
    """

    return random.randint(1, 100_000)


def generate_random_float() -> float:
    """
    Generates a random float of fixed length.
    """

    return random.uniform(1, 100_000)


def generate_random_bool() -> bool:
    """
    Generates a random boolean
    """

    return random.choice([True, False])


def generate_utc_datetime() -> datetime:
    """
    Generates a datetime with timezone UTC
    """

    return datetime.now(timezone.utc)
