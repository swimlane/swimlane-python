from functools import total_ordering

import pendulum
import six

from swimlane.core.resources.base import APIResource
from swimlane.exceptions import UnknownField, ValidationError


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
            self.id = self.tracking_id = self.created = self.modified = None
        else:
            self.id = self._raw['id']

            # Combine app acronym + trackingId instead of using trackingFull raw
            # for guaranteed value (not available through report results)
            self.tracking_id = '-'.join([
                self._app.acronym,
                str(int(self._raw['trackingId']))
            ])

            self.created = pendulum.parse(self._raw['createdDate'])
            self.modified = pendulum.parse(self._raw['modifiedDate'])

        self._fields = {}
        self.__premap_fields()

    def __str__(self):
        if self.is_new:
            return '{} - New'.format(self._app.acronym)

        return str(self.tracking_id)

    def __setitem__(self, field_name, value):
        self.get_field(field_name).set_python(value)

    def __getitem__(self, field_name):
        return self.get_field(field_name).get_python()

    def __delitem__(self, field_name):
        self[field_name] = None

    def __iter__(self):
        for field_name, field in six.iteritems(self._fields):
            yield field_name, field.get_python()

    def __hash__(self):
        return hash((self.id, self._app))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and hash(self) == hash(other)

    def __lt__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError("Comparisons not supported between instances of '{}' and '{}'".format(
                other.__class__.__name__,
                self.__class__.__name__
            ))

        tracking_number_self = int(self.tracking_id.split('-')[1])
        tracking_number_other = int(other.tracking_id.split('-')[1])

        return (self._app.name, tracking_number_self) < (other._app.name, tracking_number_other)

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

    def get_field(self, field_name):
        """Returns field instance or raises UnknownField"""
        try:
            return self._fields[field_name]
        except KeyError:
            raise UnknownField(self._app, field_name, self._fields.keys())

    def validate(self):
        """Explicitly validate field data. Called automatically during save call before sending data to server
        
        Returns None or raises ValidationError
        """
        for field in (_field for _field in six.itervalues(self._fields) if _field.required):
            if field.get_swimlane() is None:
                raise ValidationError(self, 'Required field "{}" is not set'.format(field.name))

    def save(self):
        """Persist record changes on Swimlane server
        
        Updates internal raw data with response content from server to guarantee calculated field values match values on
        server
        
        Raises ValidationError if any fields fail validation
        """

        if self.is_new:
            method = 'post'
        else:
            method = 'put'

        self.validate()

        response = self._swimlane.request(
            method,
            'app/{}/record'.format(self._app.id),
            json=self._raw
        )

        # Reinitialize record with new raw content returned from server to update any calculated fields
        self.__init__(self._app, response.json())


def record_factory(app):
    """Return a temporary Record instance to be used for field validation and value parsing"""
    # pylint: disable=line-too-long
    return Record(app, {
        '$type': Record._type,
        'isNew': True,
        'applicationId': app.id,
        'comments': {
            '$type': 'System.Collections.Generic.Dictionary`2[[System.String, mscorlib],[System.Collections.Generic.List`1[[Core.Models.Record.Comments, Core]], mscorlib]], mscorlib'
        },
        'values': {
            '$type': 'System.Collections.Generic.Dictionary`2[[System.String, mscorlib],[System.Object, mscorlib]], mscorlib'
        }
    })
