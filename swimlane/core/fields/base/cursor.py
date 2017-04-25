import weakref

from .field import Field
from swimlane.core.resources import APIResourceAdapter


class FieldCursor(APIResourceAdapter):
    """Base class for cursors encapsulating a field's complex logic potentially requiring additional request(s)"""

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
        for el in self._evaluate():
            yield el

    def __getitem__(self, item):
        return self._evaluate()[item]

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
        return []

    def get_python(self):
        """Create, cache, and return the appropriate cursor instance"""
        if self._cursor is None:
            if self.cursor_class is None:
                raise NotImplementedError('Must set "cursor_class" on {}'.format(self.__class__.__name__))

            self._cursor = self.cursor_class(self, self.get_initial_elements())

        return self._cursor

