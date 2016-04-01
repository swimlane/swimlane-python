"""This module provides a SearchResults class."""

from types import GeneratorType
from ..resources import Record, StatsResult
from ..swimlane_dict import SwimlaneDict


__metaclass__ = type


class SearchResult:
    """A class that wraps a Swimlane search result."""

    def __init__(self, report, resp):
        """Init a SearchResult.

        Args:
            report (Report): The report that was used to initiate the search.
            resp (SwimlaneDict): The JSON response from a search request.
        """
        self.is_stats = isinstance(resp, GeneratorType)
        if self.is_stats:
            self.stats = (StatsResult(SwimlaneDict(r)) for r in resp)
        else:
            self.report = report
            self.count = resp["count"]
            self.offset = resp["offset"]
            self.limit = resp["limit"]
            results = []
            if report.applicationIds[0] in resp['results']:
                results = resp["results"][report.applicationIds[0]]
            self.records = (Record(SwimlaneDict(r)) for r in results)
