from swimlane.core.resources.record import RecordAdapter
from .base import APIResourceAdapter, APIResource


class AppAdapter(APIResourceAdapter):
    """Abstracts app-level API consumption"""

    def get(self, tracking_id=None, name=None, acronym=None):
        if len(list(filter(None, (name, tracking_id, acronym)))) != 1:
            raise ValueError('Must provide only one of name, tracking_id, or acronym')

        if tracking_id:
            return App(
                self.swimlane,
                self.swimlane.api('get', 'app/{}'.format(tracking_id)).json()
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
        response = self.swimlane.api('get', 'app')
        return [App(self.swimlane, item) for item in response.json()]


class App(APIResource):
    """Represents a single App record"""

    _type = 'Core.Models.Application.Application, Core'

    def __init__(self, swimlane, raw):
        super(App, self).__init__(swimlane, raw)

        self.acronym = self._raw.get('acronym')
        self.name = self._raw.get('name')
        self.description = self._raw.get('description')
        self.fields = self._raw.get('fields')
        self.id_ = self._raw.get('id')
        self.tracking_id = self._raw.get('trackingFieldId')

        self.records = RecordAdapter(self)

    def __str__(self):
        return '{}: {}'.format(self.acronym, self.name)
