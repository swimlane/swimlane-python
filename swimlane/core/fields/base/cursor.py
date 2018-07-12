import weakref

from swimlane.core.cursor import Cursor
from swimlane.core.resolver import SwimlaneResolver
from .field import Field


class FieldCursor(Cursor, SwimlaneResolver):
    """Base class for encapsulating a field instance's complex logic
    
    Useful in abstracting away extra request(s), lazy evaluation, pagination, intensive calculations, etc.
    """

    def __init__(self, field, initial_elements=None):
        SwimlaneResolver.__init__(self, field.record._swimlane)
        Cursor.__init__(self)

        self._elements = initial_elements or self._elements

        self.__field_name = field.name
        self.__record_ref = weakref.ref(field.record)
        self.__field_ref = weakref.ref(field)

    def __repr__(self):
        # pylint: disable=missing-format-attribute
        return '<{self.__class__.__name__}: {self._record!r}["{self._field.name}"] ({length})>'.format(
            self=self,
            length=len(self)
        )

    def __eq__(self, other):
        return isinstance(other, self.__class__) and other._record.id == self._record.id

    def _sync_field(self):
        """Set source field value to current cursor value"""
        self._field.set_python(self._evaluate())

    @property
    def _record(self):
        return self.__record_ref()

    @property
    def _field(self):
        field = self.__field_ref()
        # Occurs when a record is saved and reinitialized, creating new Field instances and losing the existing weakref
        # Update weakref to point to new Field instance of the same name
        if field is None:
            field = self._record.get_field(self.__field_name)
            self.__field_ref = weakref.ref(field)
        return field


class CursorField(Field):
    """Returns a proxy-like FieldCursor instance to support additional functionality"""

    cursor_class = None

    def __init__(self, *args, **kwargs):
        super(CursorField, self).__init__(*args, **kwargs)

        self._cursor = None

    def get_initial_elements(self):
        """Return initial elements to be passed with cursor instantiation"""
        return self._get()

    def _set(self, value):
        self._cursor = None
        super(CursorField, self)._set(value)

    @property
    def cursor(self):
        """Cache and return cursor_class instance"""
        if self._cursor is None:
            # pylint: disable=not-callable
            self._cursor = self.cursor_class(self, self.get_initial_elements())

        return self._cursor

    def get_python(self):
        """Create, cache, and return the appropriate cursor instance"""
        return self.cursor
