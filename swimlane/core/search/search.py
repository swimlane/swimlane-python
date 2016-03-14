"""This module provides a search API."""

from ..auth import Client
from ..resources import StatsReport
from .search_result import SearchResult


__metaclass__ = type


class Search:
    """A class for searching Swimlane records."""

    def __init__(self, report):
        """Init a Search.

        Args:
            report (Report): The Report or StatsReport to search with.
        """
        self.report = report
        self.has_more_pages = False

    def execute(self):
        """Execute the search.

        Returns:
            A SearchResult.
        """
        url = "search"
        if isinstance(self.report, StatsReport):
            url += "/stats"
        result = SearchResult(self.report, Client.post(self.report, url))
        if not result.is_stats:
            self.report.offset += 1
            self.has_more_pages = (result.count >
                                   self.report.offset * self.report.pageSize)
        return result

    def next_page(self):
        """Retrieve the next page of results from the search.

        Returns:
            A SearchResult.
        """
        return self.execute()
