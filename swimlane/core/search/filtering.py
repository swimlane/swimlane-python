"""This module provides operators and functions for filtering."""

EQ = "equals"
NOT_EQ = "doesNotEqual"
CONTAINS = "contains"
EXCLUDES = "excludes"


def create_filter(field_id, filter_type, value):
    """Create a Filter.

    Args:
        field_id (str): The field ID.
        filter_type (str): The type of filter.
        value (str): The value to filter on.

    Returns:
        A dict representing the filter.
    """
    return {
        "fieldId": field_id,
        "filterType": filter_type,
        "value": value,
    }
