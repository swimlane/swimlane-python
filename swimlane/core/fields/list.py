from numbers import Number

import six
from shortid import ShortId

from swimlane.core.fields.base import FieldCursor
from swimlane.exceptions import ValidationError
from .base import CursorField

SID = ShortId()


class _ListFieldCursor(FieldCursor):
    """Base class for Text and Numeric FieldCursors emulating a basic list"""

    def _validate_list(self, target):
        """Validate a list against field validation rules"""
        # Check list length restrictions
        min_items = self._field.field_definition.get('minItems')
        max_items = self._field.field_definition.get('maxItems')

        if min_items is not None:
            if len(target) < min_items:
                raise ValidationError(
                    self._record,
                    "Field '{}' must have a minimum of {} item(s)".format(self._field.name, min_items)
                )

        if max_items is not None:
            if len(target) > max_items:
                raise ValidationError(
                    self._record,
                    "Field '{}' can only have a maximum of {} item(s)".format(self._field.name, max_items)
                )

        # Individual item validation
        for item in target:
            self._validate_item(item)

    def _validate_item(self, item):
        """Validate individual item against field rules. Defaults to no-op"""

    def __getattr__(self, item):
        """Fallback to any builtin list methods on self._elements for any undefined methods called on cursor

        List methods are wrapped in a function ensuring the updated value passes field validation before actually
        applying to the internal value

        Wrapper function creates a copy of the current elements in the cursor, calls whatever list method was executed
        on the copy, then validates the updated list against field rules.

        If validation fails, raise ValidationError, otherwise update the cursor elements and field value to the modified
        list copy
        """
        try:
            # Check for method on list class
            func = getattr(list, item)

            # Create a copy of elements if function exists to be the actual target of the method call
            elements_copy = self._elements[:]

            # Wrap in function adding validation after the method is executed
            def wrapper(*args, **kwargs):
                # Execute method against the copied elements
                result = func(elements_copy, *args, **kwargs)

                # Validate elements copy after any potential modification
                self._validate_list(elements_copy)

                # Update internal cursor elements to modified copy and sync with field
                self._elements = elements_copy
                self._sync_field()

                # Return in case of methods retrieving values instead of modifying state
                return result

            return wrapper
        except AttributeError:
            # Raise separate AttributeError with correct class reference instead of list
            raise AttributeError("{} object has no attribute {}".format(self.__class__, item))


class TextListFieldCursor(_ListFieldCursor):
    """Cursor for Text ListField"""

    def _validate_item(self, item):
        """Validate char/word count"""
        if not isinstance(item, six.string_types):
            raise ValidationError(
                self._record,
                "Text list field items must be strings, not '{}'".format(item.__class__)
            )

        words = item.split(' ')

        item_length_type = self._field.field_definition.get('itemLengthType')
        item_max_length = self._field.field_definition.get('itemMaxLength')
        item_min_length = self._field.field_definition.get('itemMinLength')
        if item_length_type is not None:
            # Min/max word count
            if item_length_type == 'words':
                if item_max_length is not None:
                    if len(words) > item_max_length:
                        raise ValidationError(
                            self._record,
                            "Field '{}' items cannot contain more than {} words".format(
                                self._field.name,
                                item_max_length
                            )
                        )
                if item_min_length is not None:
                    if len(words) < item_min_length:
                        raise ValidationError(
                            self._record,
                            "Field '{}' items must contain at least {} words".format(
                                self._field.name,
                                item_min_length
                            )
                        )

            # Min/max char count of full item
            else:
                if item_max_length is not None:
                    if len(item) > item_max_length:
                        raise ValidationError(
                            self._record,
                            "Field '{}' items cannot contain more than {} characters".format(
                                self._field.name,
                                item_max_length
                            )
                        )
                if item_min_length is not None:
                    if len(item) < item_min_length:
                        raise ValidationError(
                            self._record,
                            "Field '{}' items must contain at least {} characters".format(
                                self._field.name,
                                item_min_length
                            )
                        )


class NumericListFieldCursor(_ListFieldCursor):
    """Cursor for Numeric ListField"""

    def _validate_item(self, item):
        if not isinstance(item, Number):
            raise ValidationError(
                self._record,
                "Numeric list field items must be numbers, not '{}'".format(item.__class__)
            )

        # range restrictions
        item_max = self._field.field_definition.get('itemMax')
        item_min = self._field.field_definition.get('itemMin')

        if item_max is not None:
            if item > item_max:
                raise ValidationError(
                    self._record,
                    "Field '{}' items cannot be greater than {}".format(
                        self._field.name,
                        item_max
                    )
                )

        if item_min is not None:
            if item < item_min:
                raise ValidationError(
                    self._record,
                    "Field '{}' items cannot be less than {}".format(
                        self._field.name,
                        item_min
                    )
                )


class ListField(CursorField):
    """Text and Numeric List field"""

    field_type = (
        'Core.Models.Fields.List.ListField, Core',
        'Core.Models.Fields.ListField, Core',
    )

    _type_map = {
        'numeric': {
            'list_item_type': 'Core.Models.Record.ListItem`1[[System.Double, mscorlib]], Core',
            'cursor_class': NumericListFieldCursor
        },
        'text': {
            'list_item_type': 'Core.Models.Record.ListItem`1[[System.String, mscorlib]], Core',
            'cursor_class': TextListFieldCursor
        }
    }

    def __init__(self, *args, **kwargs):
        super(ListField, self).__init__(*args, **kwargs)
        self.cursor_class = self._type_map[self.input_type]['cursor_class']

    def set_swimlane(self, value):
        """Convert from list of dicts with values to list of values"""
        value = [d['value'] for d in value or []]

        return super(ListField, self).set_swimlane(value)

    def set_python(self, value):
        """Validate using cursor for consistency between direct set of values vs modification of cursor values"""
        if not isinstance(value, (list, type(None))):
            raise ValidationError(
                self.record,
                "Field '{}' must be set to a list, not '{}'".format(
                    self.name,
                    value.__class__
                )
            )
        value = value or []
        self.cursor._validate_list(value)
        return super(ListField, self).set_python(value)

    def cast_to_swimlane(self, value):
        value = super(ListField, self).cast_to_swimlane(value)
        return [self._build_list_item(item) for item in value] or None

    def cast_to_bulk_modify(self, value):
        """List fields use raw list values for bulk modify"""
        self.validate_value(value)
        return value

    def _build_list_item(self, item_value):
        """Return a dict with random ID and $type for API representation of value"""
        return {
            '$type': self._type_map[self.input_type]['list_item_type'],
            'id': SID.generate(),
            'value': item_value
        }

