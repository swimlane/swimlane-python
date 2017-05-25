import weakref

from swimlane.core.resolver import SwimlaneResolver
from .field import Field


class FieldCursor(SwimlaneResolver):
    """Base class for encapsulating a field instance's complex logic
    
    Useful in abstracting away extra request(s), lazy evaluation, pagination, intensive calculations, etc.
    """

    def __init__(self, field, initial_elements=None):
        super(FieldCursor, self).__init__(field.record._swimlane)

        self.__record_ref = weakref.ref(field.record)
        self.__field_ref = weakref.ref(field)

        self._elements = initial_elements or []

    def __repr__(self):
        return '<{self.__class__.__name__}: {self._record} ({length})>'.format(self=self, length=len(self))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and other._record.id == self._record.id

    def __len__(self):
        return len(self._evaluate())

    def __iter__(self):
        for element in self._evaluate():
            yield element

    def __getitem__(self, item):
        return self._evaluate()[item]

    def _sync_field(self):
        """Set source field value to current cursor value"""
        self._field.set_python(self._evaluate())

    def _evaluate(self):
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
    """Returns a proxy-like FieldCursor instance to support additional functionality"""

    cursor_class = None

    def __init__(self, *args, **kwargs):
        super(CursorField, self).__init__(*args, **kwargs)

        self._cursor = None

    def get_initial_elements(self):
        """Return initial elements to be passed with cursor instantiation"""
        return self._get()

    def get_python(self):
        """Create, cache, and return the appropriate cursor instance"""
        if self._cursor is None:
            # pylint: disable=not-callable
            self._cursor = self.cursor_class(self, self.get_initial_elements())

        return self._cursor

