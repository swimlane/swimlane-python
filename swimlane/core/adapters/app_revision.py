from swimlane.core.cache import check_cache
from swimlane.core.resolver import AppResolver
from swimlane.core.resources.app_revision import AppRevision
from swimlane.utils import one_of_keyword_only


class AppRevisionAdapter(AppResolver):
    """Handles retrieval of Swimlane App Revision resources"""

    def get_all(self):
        """
        Gets all app revisions.

        Returns:
            AppRevision[]: Returns all AppRevisions for this Adapter's app.
        """
        raw_revisions = self._swimlane.request('get', 'app/{0}/history'.format(self._app.id)).json()
        return [AppRevision(self._swimlane, raw) for raw in raw_revisions]

    def get(self, revision_number):
        """
        Gets a specific app revision.

        Supports resource cache

        Keyword Args:
            revision_number (float): App revision number

        Returns:
            AppRevision: The AppRevision for the given revision number.
        """
        key_value = AppRevision.get_unique_id(self._app.id, revision_number)
        return self.__get(app_id_revision=key_value)

    @check_cache(AppRevision)
    @one_of_keyword_only('app_id_revision')
    def __get(self, key, value):
        """Underlying get method supporting resource cache."""
        app_id, revision_number = AppRevision.parse_unique_id(value)
        app_revision_raw = self._swimlane.request('get', 'app/{0}/history/{1}'.format(app_id, revision_number)).json()
        return AppRevision(self._swimlane, app_revision_raw)
