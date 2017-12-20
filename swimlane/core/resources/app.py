from functools import total_ordering

import six

from swimlane.exceptions import UnknownField
from .base import APIResource


@total_ordering
class App(APIResource):
    """A single App record instance

    Used lookup field definitions and retrieve/create child Record instances

    Attributes:
        name (str): App name
        acronym (str): App acronym
        description (str): App description
        id (str): Full App ID
        tracking_id (str): App tracking ID
        records (RecordAdapter): :class:`~swimlane.core.adapters.record.RecordAdapter` configured for current App
        reports (ReportAdapter): :class:`~swimlane.core.adapters.report.ReportAdapter` configured for current App
    """

    _type = 'Core.Models.Application.Application, Core'

    def __init__(self, swimlane, raw):
        super(App, self).__init__(swimlane, raw)

        self.acronym = self._raw['acronym']
        self.name = self._raw['name']
        self.description = self._raw.get('description', '')
        self.id = self._raw['id']
        self.tracking_id = self._raw.get('trackingFieldId')

        self._fields_by_id = {f['id']: f for f in self._raw['fields']}
        self._fields_by_name = {f['name']: f for f in self._raw['fields']}
        self._keys_to_field_names = {}
        for name, field_def in six.iteritems(self._fields_by_name):
            # Include original name to simplify name resolution
            self._keys_to_field_names[name] = name
            key = field_def.get('key')
            if key:
                self._keys_to_field_names[key] = name

        # Avoid circular import
        from swimlane.core.adapters import RecordAdapter, ReportAdapter
        self.records = RecordAdapter(self)
        self.reports = ReportAdapter(self)

    def __str__(self):
        return '{self.name} ({self.acronym})'.format(self=self)

    def __hash__(self):
        return hash((self.id, self.name))

    def __lt__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError("Comparisons not supported between instances of '{}' and '{}'".format(
                other.__class__.__name__,
                self.__class__.__name__
            ))

        return self.name < other.name

    def get_cache_index_keys(self):
        """Return all fields available when retrieving apps"""
        return {
            'id': self.id,
            'name': self.name,
            'acroynm': self.acronym
        }

    def resolve_field_name(self, field_key):
        """Return the field name matching the given key or None. Searches field keys first, falls back to field names"""
        return self._keys_to_field_names.get(field_key)

    def get_field_definition_by_name(self, field_name):
        """Get JSON field definition for field matching provided name

        Args:
            field_name (str): Target field name to get definition for

        Raises:
            swimlane.exceptions.UnknownField: Raised when given a field name not found in App

        Returns:
            dict: Field metadata definition
        """
        try:
            return self._fields_by_name[field_name]
        except KeyError:
            raise UnknownField(self, field_name, self._fields_by_name.keys())

    def get_field_definition_by_id(self, field_id):
        """Get JSON field definition for field matching provided id

        Args:
            field_id (str): Target field ID to get definition for

        Raises:
            swimlane.exceptions.UnknownField: Raised when given a field ID not found in App

        Returns:
            dict: Field metadata definition
        """
        try:
            return self._fields_by_id[field_id]
        except KeyError:
            raise UnknownField(self, field_id, self._fields_by_id.keys())
