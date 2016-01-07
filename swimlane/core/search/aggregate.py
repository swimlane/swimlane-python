"""This module provides operators and functions for aggregating."""

AVG = "average"
COUNT = "count"
SUM = "sum"
MIN = "min"
MAX = "max"


def create_aggregate(field_id, aggregate_type):
    """Create an aggregate..

    Args:
        field_id (str): The field ID.
        aggregate_type (str): The type of aggregate..

    Returns:
        A dict representing the aggregate..
    """
    return {
        "fieldId": field_id,
        "aggregateType": aggregate_type
    }

