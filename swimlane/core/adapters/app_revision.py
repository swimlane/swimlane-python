from swimlane.core.cache import check_cache
from swimlane.core.resolver import AppResolver
from swimlane.core.resources.app_revision import AppRevision


class AppRevisionAdapter(AppResolver):
    """Handles retrieval and creation of Swimlane App Revision resources"""

    @check_cache(AppRevision)
    def get(self, revision_number):
        """Gets a specific app revision.

        Supports resource cache

        Keyword Args:
            revision_number (float): App revision number

        Returns:
            AppRevision: The AppRevision for the given revision number.
        """

        app_revision_raw = self._swimlane.request('get', 'app/{0}/history/{1}'.format(self._app.id,
                                                                                      revision_number)).json()
        return AppRevision(self._swimlane, app_revision_raw)
