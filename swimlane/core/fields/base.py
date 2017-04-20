"""Base classes used to build field abstractions"""
import weakref

from swimlane.core.resources import APIResourceAdapter


class Field(object):
    """Base class for abstracting Swimlane complex types"""

    _field_type = None
    _resource_type = None

    # Sentinel representing a field that has no current value
    _unset = object()

    # List of supported types, leave blank to disable type validation
    supported_types = []

    def __init__(self, name, record, default_value=_unset, allow_null=True):
        self.name = name
        self.__record_ref = weakref.ref(record)
        self.default = default_value
        self.allow_null = allow_null
        self._value = self.default

        self.field_definition = self.record._app.get_field_definition_by_name(self.name)
        self.id = self.field_definition['id']

    def __repr__(self):
        return '<{class_name}: {py!r}>'.format(class_name=self.__class__.__name__, py=self.get_python())

    @property
    def record(self):
        return self.__record_ref()

    def _get(self):
        """Default getter used for both representations unless overridden"""
        return self._value

    def get_python(self):
        """Return best python representation of field value"""
        return self._get()

    def get_swimlane(self):
        """Return best swimlane representation of field value"""
        return self._get()

    def _validate_value(self, value):
        """Validate value is an acceptable type"""
        if value is None:
            if not self.allow_null:
                raise ValueError('Field "{}" does not allow null and cannot be set to None')
        else:
            if self.supported_types and not isinstance(value, tuple(self.supported_types)):
                raise TypeError('Field "{}" expects one of "{}", got "{}" instead'.format(
                    self.name,
                    ', '.join([t.__name__ for t in self.supported_types]),
                    type(value).__name__)
                )

    def _set(self, value):
        """Default setter used for both representations unless overridden"""
        self._validate_value(value)
        self._value = value

    def set_python(self, value):
        """Set field internal value from the python representation of field value"""
        return self._set(value)

    def set_swimlane(self, value):
        """Set field internal value from the swimlane representation of field value"""
        return self._set(value)

    def unset(self):
        """Marks field as having no particular value"""
        self._value = self.default


class ReadOnly(object):
    """Mixin disabling setting value via python"""

    def set_python(self, value):
        """Disable user updating value. Raises AttributeError to emulate @property/__slots__ behavior"""
        raise AttributeError('Cannot manually set field "{}"'.format(self.name))


class RecordCursor(APIResourceAdapter):
    """Base class for objects encapsulating a record's complex fields potentially requiring additional request(s)"""

    def __init__(self, field):
        super(RecordCursor, self).__init__(field.record._swimlane)

        self.__record_ref = weakref.ref(field.record)
        self.__field_ref = weakref.ref(field)

        self._elements = []

    def __repr__(self):
        return '<{self.__class__.__name__}: {self._record} ({length})>'.format(self=self, length=len(self))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and other._record.id == self._record.id

    def __len__(self):
        return len(self.elements)

    def __iter__(self):
        for el in self.elements:
            yield el

    @property
    def elements(self):
        """Hook to allow lazy evaluation or retrieval of cursor's elements
        
        Defaults to simply returning list of self._elements
        """
        return self._elements

    @property
    def _record(self):
        return self.__record_ref()

    @property
    def _field(self):
        return self.__field_ref()


class CursorField(Field):
    """Returns a proxy-like RecordCursor instance to allow encapsulation of value and extension of functionality"""

    cursor_class = None

    def __init__(self, *args, **kwargs):
        super(CursorField, self).__init__(*args, **kwargs)

        self._cursor = None

    def get_python(self):
        """Create, cache, and return the appropriate cursor instance"""
        if self._cursor is None:
            if self.cursor_class is None:
                raise NotImplementedError('Must set "cursor_class" on {}'.format(self.__class__.__name__))

            self._cursor = self.cursor_class(self)

        return self._cursor
