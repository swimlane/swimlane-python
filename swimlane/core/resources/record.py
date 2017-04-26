import json
import weakref
from functools import total_ordering

import six

from swimlane.core.resources.base import APIResource, SwimlaneResolver
from swimlane.errors import UnknownField
from swimlane.utils import random_string


class RecordAdapter(SwimlaneResolver):
    """Allows retrieval and creation of Swimlane records"""

    def __init__(self, app):
        super(RecordAdapter, self).__init__(app._swimlane)

        self.__ref_app = weakref.ref(app)

    @property
    def _app(self):
        """Resolve app weak reference"""
        return self.__ref_app()

    def get(self, **kwargs):
        """Get a single record by full id"""
        record_id = kwargs.pop('id', None)

        if kwargs:
            raise TypeError('Unexpected arguments: {}'.format(kwargs))

        if record_id is None:
            raise TypeError('Must provide id argument')

        response = self._swimlane.request('get', "app/{0}/record/{1}".format(self._app.id, record_id))

        return Record(self._app, response.json())

    def search(self, *filter_tuples):
        """Shortcut to generate a new temporary search report using provided filters and return the results"""
        report = self._app.reports.create('search-' + random_string(8))

        for filter_tuple in filter_tuples:
            report.filter(*filter_tuple)

        return list(report)

    def create(self, **fields):
        """Create and return a new record in associated app and return the corresponding Record instance
        
        Arguments should be field names with their respective python values
        """
        # Use temporary Record instance to build fields and inject python values
        #pylint: disable=line-too-long
        new_record = Record(self._app, {
            '$type': Record._type,
            'isNew': True,
            'applicationId': self._app.id,
            'comments': {
                '$type': 'System.Collections.Generic.Dictionary`2[[System.String, mscorlib],[System.Collections.Generic.List`1[[Core.Models.Record.Comments, Core]], mscorlib]], mscorlib'
            },
            'values': {
                '$type': 'System.Collections.Generic.Dictionary`2[[System.String, mscorlib],[System.Object, mscorlib]], mscorlib'
            }
        })

        for field_name, field_value in six.iteritems(fields):
            new_record[field_name] = field_value

        # Send converted data to server
        response = self._swimlane.request(
            'post',
            'app/{}/record'.format(self._app.id),
            data=new_record.serialize()
        )

        # Return new Record instance from returned data
        return Record(self._app, response.json())


@total_ordering
class Record(APIResource):
    """A Swimlane record"""

    _type = 'Core.Models.Record.Record, Core'

    def __init__(self, app, raw):
        super(Record, self).__init__(app._swimlane, raw)

        self._app = app

        self.is_new = self._raw.get('isNew', False)

        # Protect against creation from generic raw data not yet containing server-generated values
        if self.is_new:
            self.id = self.tracking_id = None
        else:
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
            raise UnknownField(self._app, field_name, self._fields.keys())

        field.set_python(value)

    def __getitem__(self, field_name):
        field = self._fields.get(field_name)

        if field is None:
            raise UnknownField(self._app, field_name, self._fields.keys())

        return field.get_python()

    def __delitem__(self, field_name):
        field = self._fields.get(field_name)

        if field is None:
            raise UnknownField(self._app, field_name, self._fields.keys())

        field.unset()

    def __iter__(self):
        for field_name, field in six.iteritems(self._fields):
            yield field_name, field.get_python()

    def __hash__(self):
        return hash((self.id, self._app))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and hash(self) == hash(other)

    def __lt__(self, other):
        return isinstance(other, self.__class__) and (self.id, self._app.id) < (other.id, other._app.id)

    def __premap_fields(self):
        """Build field instances using field definitions in app manifest
        
        Map raw record field data into appropriate field instances with their correct respective types
        """
        # Circular imports
        from swimlane.core.fields import resolve_field_class

        for field_definition in self._app._raw['fields']:
            field_class = resolve_field_class(field_definition)

            field_instance = field_class(field_definition['name'], self)
            value = self._raw['values'].get(field_instance.id)
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
        # Use "data=" vs "json=" to control serialization (primarily for ordered keys with $type key first)
        self._swimlane.request(
            'put',
            'app/{}/record'.format(self._app.id),
            data=self.serialize()
        )
