from .base import APIResourceAdapter, APIResource

from swimlane.core.resources.record import RecordAdapter
from swimlane.core.resources.report import ReportAdapter


class AppAdapter(APIResourceAdapter):
    """Abstracts app-level API consumption"""

    def get(self, tracking_id=None, name=None, acronym=None):
        if len(list(filter(None, (name, tracking_id, acronym)))) != 1:
            raise ValueError('Must provide only one of name, tracking_id, or acronym')

        if tracking_id:
            return App(
                self._swimlane,
                self._swimlane.request('get', 'app/{}'.format(tracking_id)).json()
            )
        else:
            # Workaround for lack of support for get by name or acronym
            for app in self.list():
                if any([
                    name and name == app.name,
                    acronym and acronym == app.acronym
                ]):
                    return app

    def list(self):
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

        self._fields = {f['name']: f for f in self._raw['fields']}

        self.records = RecordAdapter(self)
        self.reports = ReportAdapter(self)

    def __str__(self):
        return '{self.name} ({self.acronym})'.format(self=self)

    def get_field_definition(self, field_name):
        try:
            return self._fields[field_name]
        except KeyError as e:
            e.message = 'Unable to find field "{}"'.format(field_name)
            raise
