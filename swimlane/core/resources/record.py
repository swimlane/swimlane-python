import json
from functools import total_ordering

import six

from swimlane.core.resources.base import APIResource
from swimlane.errors import UnknownField


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
