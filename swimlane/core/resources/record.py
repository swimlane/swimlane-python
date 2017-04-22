import json
import weakref

import six

from swimlane.core.fields import resolve_field_class
from swimlane.core.resources.base import APIResource, APIResourceAdapter
from swimlane.utils import random_string


class RecordAdapter(APIResourceAdapter):
    """Allows retrieval and creation of Swimlane records"""

    def __init__(self, app):
        super(RecordAdapter, self).__init__(app._swimlane)

        self.__ref_app = weakref.ref(app)

    @property
    def _app(self):
        return self.__ref_app()

    def get(self, **kwargs):
        """Get a single record by full id"""
        record_id = kwargs.pop('id', None)

        if kwargs:
            raise TypeError('Unexpected **kwargs: {}'.format(kwargs))

        if record_id is None:
            raise TypeError('Must provide id argument')

        response = self._swimlane.request('get', "app/{0}/record/{1}".format(self._app.id, record_id))

        return Record(self._app, response.json())

    def search(self, *filters):
        """Shortcut to generate a new temporary search report using provided filters and return the results"""
        report = self._app.reports.create('search-' + random_string(8))

        for f in filters:
            report.filter(*f)

        # TODO: Delete report after retrieving results

        return list(report)

    def create(self, **fields):
        """Create a new record in associated app and return the corresponding Record instance"""
        raise NotImplementedError
        response = self._swimlane.request(
            'post',
            'app/{}/record'.format(self._app.id),

        )


class Record(APIResource):

    _type = 'Core.Models.Record.Record, Core'

    def __init__(self, app, raw):
        super(Record, self).__init__(app._swimlane, raw)

        self._app = app

        self.id = self._raw['id']

        # Combine app acronym + trackingId instead of using trackingFull raw
        # for guaranteed value (not available through report results)
        self.tracking_id = '-'.join([
            self._app.acronym,
            str(int(self._raw['trackingId']))
        ])

        self._fields = {}
        self.__premap_fields()

    def __str__(self):
        return str(self.tracking_id)

    def __setitem__(self, field_name, value):
        field = self._fields.get(field_name)

        if field is None:
            raise KeyError('Unknown field "{}"'.format(field_name))

        field.set_python(value)

    def __getitem__(self, field_name):
        field = self._fields.get(field_name)

        if field is None:
            raise KeyError('Unknown field "{}"'.format(field_name))

        return field.get_python()

    def __delitem__(self, field_name):
        field = self._fields.get(field_name)

        if field is None:
            raise KeyError('Unknown field "{}"'.format(field_name))

        field.unset()

    def __iter__(self):
        for field_name, field in six.iteritems(self._fields):
            yield field_name, field.get_python()

    def __premap_fields(self):
        """Build field instances using field definitions in app manifest
        
        Map raw record field data into appropriate field instances with their correct respective types
        """
        for field_definition in self._app._raw['fields']:
            field_class = resolve_field_class(field_definition)

            field_instance = field_class(field_definition['name'], self)
            try:
                value = self._raw['values'].get(field_instance.id)
            except KeyError:
                pass
            else:
                field_instance.set_swimlane(value)

            self._fields[field_instance.name] = field_instance

    def serialize(self):
        """Serialize record to JSON string for use in Swimlane save call"""
        return json.dumps(
            self._raw,
            sort_keys=True,
            separators=(',', ':')
        )

    def save(self):
        """Update record in Swimlane"""
        self._swimlane.request(
            'put',
            'app/{}/record'.format(self._app.id),
            data=self.serialize()
        )
