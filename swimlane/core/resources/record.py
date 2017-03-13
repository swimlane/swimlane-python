from swimlane.core.resources.base import APIResource, APIResourceAdapter


class RecordAdapter(APIResourceAdapter):

    def __init__(self, app):
        super(RecordAdapter, self).__init__(app.swimlane)

        self.app = app

    def get(self, record_id):
        response = self.swimlane.api('get', "app/{0}/record/{1}".format(self.app.tracking_id, record_id))

        return Record(self.app, response.json())


class Record(APIResource):

    _type = 'Core.Models.Record.Record, Core'

    def __init__(self, app, raw):
        super(Record, self).__init__(app.swimlane, raw)

        self.app = app

        self.id = self._raw['id']
        self.tracking_full = self._raw['trackingFull']

        self.__fields = {}
        self.__premap_fields()

    def __premap_fields(self):
        """Gather field keys from app data and merge with values data from record data"""
        for field_obj in self.app._raw['fields']:
            self.__fields[field_obj['name']] = self._raw['values'].get(field_obj['id'])

    def __str__(self):
        return '{}: {}'.format(self.tracking_full, self.id)

    def __setitem__(self, key, value):
        self.__fields[key] = value

    def __getitem__(self, item):
        return self.__fields[item]

    def __delitem__(self, key):
        del self.__fields[key]

