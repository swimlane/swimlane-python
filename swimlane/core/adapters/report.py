import weakref

from swimlane.core.resolver import SwimlaneResolver
from swimlane.core.resources.report import Report, report_factory


class ReportAdapter(SwimlaneResolver):
    """Handles retrieval and creation of Report resources"""

    def __init__(self, app):
        super(ReportAdapter, self).__init__(app._swimlane)

        self.__ref_app = weakref.ref(app)

    @property
    def _app(self):
        """Resolve weak app reference"""
        return self.__ref_app()

    def list(self):
        """Retrieve all reports for parent app

        Returns:
            :class:`list` of :class:`~swimlane.core.resources.report.Report`: List of all returned reports
        """
        raw_reports = self._swimlane.request('get', "reports?appId={}".format(self._app.id)).json()
        # Ignore StatsReports for now
        return [Report(self._app, raw_report) for raw_report in raw_reports if raw_report['$type'] == Report._type]

    def get(self, report_id):
        """Retrieve report by ID

        Args:
            report_id (str): Full report ID

        Returns:
            Report: Corresponding Report instance
        """
        return Report(
            self._app,
            self._swimlane.request('get', "reports/{0}".format(report_id)).json()
        )

    def build(self, name, **kwargs):
        """Report instance factory for the adapter's App

        Args:
            name (str): New Report name

        Keyword Args:
            **kwargs: Extra keyword args passed to Report class

        Returns:
            Report: Newly created local Report instance
        """
        return report_factory(self._app, name, **kwargs)
