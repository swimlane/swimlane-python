import logging
import six
from sortedcontainers import SortedDict
from swimlane.core.fields.base import CursorField, FieldCursor
from swimlane.core.resources.record import Record
from swimlane.exceptions import ValidationError, SwimlaneHTTP400Error

logger = logging.getLogger(__name__)


class ReferenceCursor(FieldCursor):
    """Handles lazy retrieval of target records"""

    def __init__(self, *args, **kwargs):
        super(ReferenceCursor, self).__init__(*args, **kwargs)
        self._elements = self._elements or SortedDict()

    @property
    def target_app(self):
        """Make field's target_app available on cursor"""
        return self._field.target_app

    def __getitem__(self, item):
        record_id, record = [kv for kv in self._elements.items()][item]
        if record is self._field._unset:
            try:
                records_get = self.target_app.records.get(id=record_id)
                self._elements[record_id] = records_get
                return records_get
            except SwimlaneHTTP400Error:
                logger.debug('Received 400 response retrieving record "{}", ignoring assumed orphaned record')
        else:
            return record

    def __iter__(self):
        for record_id, record in six.iteritems(self._elements):
            if record is self._field._unset:
                try:
                    records_get = self.target_app.records.get(id=record_id)
                    self._elements[record_id] = records_get
                    yield records_get
                except SwimlaneHTTP400Error:
                    logger.debug('Received 400 response retrieving record "{}", ignoring assumed orphaned record')
            else:
                yield record

    def add(self, record):
        """Add a reference to the provided record"""
        self._field.validate_value(record)
        self._elements[record.id] = record
        self._sync_field()

    def remove(self, record):
        """Remove a reference to the provided record"""
        self._field.validate_value(record)
        del self._elements[record.id]
        self._sync_field()


class ReferenceField(CursorField):

    field_type = 'Core.Models.Fields.Reference.ReferenceField, Core'
    supported_types = (Record,)
    cursor_class = ReferenceCursor

    def __init__(self, *args, **kwargs):
        super(ReferenceField, self).__init__(*args, **kwargs)
        self.__target_app_id = self.field_definition['targetId']
        self.__target_app = None

    @property
    def target_app(self):
        """Defer target app retrieval until requested"""
        if self.__target_app is None:
            self.__target_app = self._swimlane.apps.get(id=self.__target_app_id)

        return self.__target_app

    def validate_value(self, value):
        """Validate provided record is a part of the appropriate target app for the field"""
        if value not in (None, self._unset):

            if value.app != self.target_app:
                raise ValidationError(
                    self.record,
                    'Reference field "{}" has target app "{}", cannot reference record "{}" from app "{}"'.format(
                        self.name,
                        self.target_app,
                        value,
                        value.app
                    )
                )

    def _set(self, value):
        self._cursor = None
        self._value = value or None

    def set_swimlane(self, value):
        """Store record ids in separate location for later use, but ignore initial value"""

        # Values come in as a list of record ids or None
        value = value or []
        if isinstance(value, dict):
            value = value["_v"] if "_v" in value else []

        records = SortedDict()

        for record_id in value:
            records[record_id] = self._unset

        return super(ReferenceField, self).set_swimlane(records)

    def set_python(self, value):
        """With changes to Lazy instrumentation _evaluation returns SortedDictionary, unfortunately this
        is still public method that can be accessed in the old way, therefore it was split in two.
        """
        if isinstance(value, SortedDict):
            self.set_python_raw(value)
        else:
            self.set_python_old(value)

    def set_python_old(self, value):
        """Expect list of record instances, convert to a SortedDict for internal representation"""
        if not self.multiselect:
            if value and not isinstance(value, list):
                value = [value]

        value = value or []

        records = SortedDict()

        for record in value:
            self.validate_value(record)
            records[record.id] = record

        self._set(records)
        self.record._raw['values'][self.id] = self.get_swimlane()

    def get_swimlane(self):
        """Return list of record ids"""
        value = super(ReferenceField, self).get_swimlane()
        if value:
            ids = list(value.keys())
            return ids

    def get_item(self):
        """Return cursor if multi-select, direct value if single-select"""
        cursor = super(ReferenceField, self).get_python()
        if self.multiselect:
            return cursor
        else:
            try:
                return cursor[0]
            except IndexError:
                return None

    def get_batch_representation(self):
        """Return best batch process representation of field value"""
        return self.get_swimlane()

    def cast_to_report(self, value):
        return value.id

    def for_json(self):
        return self.get_swimlane()

    def set_python_raw(self, value):
        self._set(value)
        self.record._raw['values'][self.id] = self.get_swimlane()
