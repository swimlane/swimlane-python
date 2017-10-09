from swimlane.core.cache import check_cache
from swimlane.core.resolver import SwimlaneResolver
from swimlane.core.resources.app import App
from swimlane.utils import one_of_keyword_only


class AppAdapter(SwimlaneResolver):
    """Handles retrieval of Swimlane App resources"""

    @check_cache(App)
    @one_of_keyword_only('id', 'name')
    def get(self, key, value):
        """Get single app by one of id or name

        Supports resource cache

        Keyword Args:
            id (str): Full app id
            name (str): App name

        Returns:
            App: Corresponding App resource instance

        Raises:
            TypeError: No or multiple keyword arguments provided
            ValueError: No matching app found on server
        """
        if key == 'id':
            # Server returns 204 instead of 404 for a non-existent app id
            response = self._swimlane.request('get', 'app/{}'.format(value))
            if response.status_code == 204:
                raise ValueError('No app with id "{}"'.format(value))

            return App(
                self._swimlane,
                response.json()
            )
        else:
            # Workaround for lack of support for get by name
            # Holdover from previous driver support, to be fixed as part of 3.x
            for app in self.list():
                if value and value == app.name:
                    return app

            # No matching app found
            raise ValueError('No app with name "{}"'.format(value))

    def list(self):
        """Retrieve list of all apps

        Returns:
            :class:`list` of :class:`~swimlane.core.resources.app.App`: List of all retrieved apps
        """
        response = self._swimlane.request('get', 'app')
        return [App(self._swimlane, item) for item in response.json()]
