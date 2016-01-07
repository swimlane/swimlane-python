"""This module provides operators and functions for grouping by a field.."""

GB = "groupBy"
HOUR = "groupByHour"
DAY = "groupByDay"
WEEK = "groupByWeek"
MONTH = "groupByMonth"
QUARTER = "groupByQuarter"
YEAR = "groupByYear"


def create_groupby(field_id, groupby_type):
    """Create a GroupBy.

    Args:
        field_id (str): The field ID.
        groupby_type (str): The type of grouping.

    Returns:
        A dict representing the groupby.
    """
    return {
        "fieldId": field_id,
        "groupByType": groupby_type
    }

