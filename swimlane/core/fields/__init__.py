"""Abstractions for Swimlane app field types to simplify getting/setting values on records"""

from six import string_types as _string_types

from swimlane.core.fields.base import Field
from swimlane.utils import (
    get_recursive_subclasses as _get_recursive_subclasses,
    import_submodules as _import_submodules
)

_import_submodules(__name__)


def _build_field_type_map(base_class):
    """Create mapping from all $type values to their respective Field classes"""
    mapping = {}

    for cls in _get_recursive_subclasses(base_class):
        if cls.field_type:
            if isinstance(cls.field_type, tuple):
                for field_type in cls.field_type:
                    mapping[field_type] = cls
            elif isinstance(cls.field_type, _string_types):
                mapping[cls.field_type] = cls
            else:
                raise ValueError('Field type must be str or tuple, cannot understand type "{}" on class "{}"'.format(
                    type(cls.field_type),
                    cls
                ))

    return mapping


_FIELD_TYPE_MAP = _build_field_type_map(Field)


def resolve_field_class(field_definition):
    """Return field class most fitting of provided Swimlane field definition"""
    try:
        return _FIELD_TYPE_MAP[field_definition['$type']]
    except KeyError as error:
        error.message = 'No field available to handle Swimlane $type "{}"'.format(field_definition)
        raise


__all__ = ['resolve_field_class'] + [f.__class__.__name__ for f in _FIELD_TYPE_MAP.values()]
