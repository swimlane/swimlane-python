"""Abstractions for Swimlane app field types to simplify getting/setting values on records"""
from swimlane.core.fields.base import Field

from swimlane.utils import (
    get_recursive_subclasses as _get_recursive_subclasses,
    import_submodules as _import_submodules
)

_import_submodules(__name__)

# Lookup corresponding field given a Swimlane "$type" key
_FIELD_TYPE_MAP = {f.field_type: f for f in _get_recursive_subclasses(Field) if f.field_type}


def resolve_field_class(field_definition):
    """Return field class most fitting of provided Swimlane field definition"""
    try:
        return _FIELD_TYPE_MAP[field_definition['$type']]
    except KeyError as error:
        error.message = 'No field available to handle Swimlane $type "{}"'.format(field_definition)
        raise


__all__ = ['resolve_field_class'] + [f.__class__.__name__ for f in _FIELD_TYPE_MAP.values()]
