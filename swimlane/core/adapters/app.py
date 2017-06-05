from swimlane.core.resolver import SwimlaneResolver
from swimlane.core.resources import App


class AppAdapter(SwimlaneResolver):
    """Handles retrieval of Swimlane App resources"""

    def get(self, **kwargs):
        """Get single app by one of id or name

        Keyword Args:
            id (str): Full app id
            name (str): App name

        Returns:
            App: Corresponding App resource instance

        Raises:
            TypeError: No or multiple keyword arguments provided
            ValueError: No matching app found on server
        """
        orig_kwargs = kwargs.copy()
        app_id = kwargs.pop('id', None)
        name = kwargs.pop('name', None)

        if kwargs:
            raise TypeError('Unexpected argument(s): {}'.format(kwargs))

        if len(orig_kwargs) != 1:
            raise TypeError('Must provide only one argument from name, id, or acronym')

        if app_id:
            # Server returns 204 instead of 404 for a non-existent app id
            response = self._swimlane.request('get', 'app/{}'.format(app_id))
            if response.status_code == 204:
                raise ValueError('No app with id = "{}"'.format(app_id))

            return App(
                self._swimlane,
                response.json()
            )
        else:
            # FIXME: Workaround for lack of support for get by name
            # Holdover from previous driver support
            for app in self.list():
                if name and name == app.name:
                    return app

            # No matching app found
            raise ValueError('No app matching provided arguments: {}'.format(orig_kwargs))

    def list(self):
        """Retrieve list of all apps

        Returns:
            :obj:`list` of :obj:`App`: List of all retrieved apps
        """
        response = self._swimlane.request('get', 'app')
        return [App(self._swimlane, item) for item in response.json()]
