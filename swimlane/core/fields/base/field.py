import weakref

from swimlane.core.resolver import SwimlaneResolver
from swimlane.exceptions import ValidationError


class Field(SwimlaneResolver):
    """Base class for abstracting Swimlane complex types"""

    field_type = None

    # Sentinel representing a field that has no current value
    _unset = object()

    # List of supported types, leave blank to disable type validation
    supported_types = []

    def __init__(self, name, record):
        """Value not included during instantiation to prevent ambiguity between python and swimlane representations"""
        super(Field, self).__init__(record._swimlane)

        self.name = name
        self.__record_ref = weakref.ref(record)
        self._value = self._unset

        self.field_definition = self.record._app.get_field_definition_by_name(self.name)
        self.id = self.field_definition['id']
        self.input_type = self.field_definition.get('inputType')
        self.required = self.field_definition.get('required', False)
        self.readonly = bool(self.field_definition.get('formula', self.field_definition.get('readOnly', False)))

    def __repr__(self):
        return '<{class_name}: {py!r}>'.format(class_name=self.__class__.__name__, py=self.get_python())

    @property
    def record(self):
        """Resolve weak reference to parent record"""
        return self.__record_ref()

    def _get(self):
        """Default getter used for both representations unless overridden"""
        return self._value

    def get_python(self):
        """Return best python representation of field value"""
        return self._get()

    def cast_to_swimlane(self, value):
        """Called during get_swimlane, should accept a python value and return swimlane representation
        
        Defaults to no-op
        """
        return value

    def get_swimlane(self):
        """Return best swimlane representation of field value"""
        return self.cast_to_swimlane(self._get())

    def validate_value(self, value):
        """Validate value is an acceptable type during _set operation"""
        if value not in (None, self._unset):
            if self.supported_types and not isinstance(value, tuple(self.supported_types)):
                raise ValidationError(self.record, "Field '{}' expects one of {}, got '{}' instead".format(
                    self.name,
                    ', '.join([repr(t.__name__) for t in self.supported_types]),
                    type(value).__name__)
                )

    def _set(self, value):
        """Default setter used for both representations unless overridden"""
        self.validate_value(value)
        self._value = value

    def set_python(self, value):
        """Set field internal value from the python representation of field value"""
        if self.readonly:
            raise ValidationError(self.record, "Cannot set readonly field '{}'".format(self.name))

        return_value = self._set(value)

        # Set raw value to expected swimlane format once internal set is successful
        self.record._raw['values'][self.id] = self.get_swimlane()

        return return_value

    def cast_to_python(self, value):
        """Called during set_swimlane, should accept a single raw value as provided from API
        
        Defaults to no-op
        """
        return value

    def set_swimlane(self, value):
        """Set field internal value from the swimlane representation of field value"""
        return self._set(self.cast_to_python(value))
