"""
Utility functions for UUID generation
"""
from uuid import UUID, uuid4


def generate_uuid() -> UUID:
    """
    Generate a new UUID
    """
    return uuid4()


def validate_uuid(uuid_str: str) -> bool:
    """
    Validate if a string is a valid UUID
    """
    try:
        UUID(uuid_str)
        return True
    except ValueError:
        return False