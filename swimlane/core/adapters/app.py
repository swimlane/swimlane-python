from swimlane.core.resolver import SwimlaneResolver
from swimlane.core.resources import App


class AppAdapter(SwimlaneResolver):
    """Allows retrieval of Swimlane Apps"""

    def get(self, **kwargs):
        """Get single app by id, name, or acronym"""
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
        """Return list of all apps"""
        response = self._swimlane.request('get', 'app')
        return [App(self._swimlane, item) for item in response.json()]
