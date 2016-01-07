"""Provides a StatsResult class."""

from .resource import Resource


class StatsResult(Resource):
    """A simple abstraction over a Swimlane stats collection."""

    def __init__(self, fields):
        """Init a StatsResult with fields.

        Args:
            fields (dict): A dict of fields and values
        """
        super(StatsResult, self).__init__(fields)
        self.groups = self._fields

