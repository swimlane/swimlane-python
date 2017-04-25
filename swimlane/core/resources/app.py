from swimlane.errors import UnknownField
from .base import SwimlaneResolver, APIResource

from swimlane.core.resources.record import RecordAdapter
from swimlane.core.resources.report import ReportAdapter


class AppAdapter(SwimlaneResolver):
    """Allows retrieval of Swimlane Apps"""

    def get(self, **kwargs):
        """Get single app by id, name, or acronym"""
        app_id = kwargs.pop('id', None)
        name = kwargs.pop('name', None)
        acronym = kwargs.pop('acronym', None)

        if kwargs:
            raise TypeError('Unexpected argument(s): {}'.format(kwargs))

        if len(list(filter(lambda x: x is not None, (name, app_id, acronym)))) != 1:
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
            # FIXME: Workaround for lack of support for get by name or acronym
            # Holdover from previous driver support
            for app in self.list():
                if any([
                    name and name == app.name,
                    acronym and acronym == app.acronym
                ]):
                    return app
            else:
                # No matching app found
                raise ValueError('No app matching provided arguments: {}'.format(kwargs))

    def list(self):
        """Return list of all apps"""
        response = self._swimlane.request('get', 'app')
        return [App(self._swimlane, item) for item in response.json()]


class App(APIResource):
    """Represents a single App record"""

    _type = 'Core.Models.Application.Application, Core'

    def __init__(self, swimlane, raw):
        super(App, self).__init__(swimlane, raw)

        self.acronym = self._raw['acronym']
        self.name = self._raw['name']
        self.description = self._raw.get('description', '')
        self.id = self._raw['id']
        self.tracking_id = self._raw.get('trackingFieldId')

        self._fields_by_name = {f['name']: f for f in self._raw['fields']}
        self._fields_by_id = {f['id']: f for f in self._raw['fields']}

        self.records = RecordAdapter(self)
        self.reports = ReportAdapter(self)

    def __str__(self):
        return '{self.name} ({self.acronym})'.format(self=self)

    def get_field_definition_by_name(self, field_name):
        """Get JSON field definition for field matching provided name"""
        try:
            return self._fields_by_name[field_name]
        except KeyError:
            raise UnknownField(self, field_name, self._fields_by_name.keys())

    def get_field_definition_by_id(self, field_id):
        """Get JSON field definition for field matching provided id"""
        try:
            return self._fields_by_id[field_id]
        except KeyError:
            raise UnknownField(self, field_id, self._fields_by_id.keys())
