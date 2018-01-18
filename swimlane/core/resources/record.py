import copy
from functools import total_ordering

import pendulum
import six

from swimlane.core.resources.base import APIResource
from swimlane.core.resources.usergroup import UserGroup
from swimlane.exceptions import UnknownField, ValidationError


@total_ordering
class Record(APIResource):
    """A single Swimlane Record instance

    Attributes:
        id (str): Full Record ID
        tracking_id (str): Record tracking ID
        created (pendulum.Pendulum): Pendulum datetime for Record created date
        modified (pendulum.Pendulum): Pendulum datetime for Record last modified date
        is_new (bool): True if Record does not yet exist on server. Other values may be temporarily None if True
        app (App): App instance that Record belongs to
    """

    _type = 'Core.Models.Record.Record, Core'

    def __init__(self, app, raw):
        super(Record, self).__init__(app._swimlane, raw)

        self.__app = app

        self.is_new = self._raw.get('isNew', False)

        # Protect against creation from generic raw data not yet containing server-generated values
        if self.is_new:
            self.id = self.tracking_id = self.created = self.modified = None
        else:
            record_app_id = raw['applicationId']
            if record_app_id != app.id:
                raise ValueError('Record applicationId `{}` does not match source app id `{}`'.format(
                    record_app_id,
                    app.id
                ))

            self.id = self._raw['id']

            # Combine app acronym + trackingId instead of using trackingFull raw
            # for guaranteed value (not available through report results)
            self.tracking_id = '-'.join([
                self.app.acronym,
                str(int(self._raw['trackingId']))
            ])

            self.created = pendulum.parse(self._raw['createdDate'])
            self.modified = pendulum.parse(self._raw['modifiedDate'])

        self.__allowed = []

        self._fields = {}
        self.__premap_fields()

    @property
    def app(self):
        return self.__app

    def __str__(self):
        if self.is_new:
            return '{} - New'.format(self.app.acronym)

        return str(self.tracking_id)

    def __setitem__(self, field_name, value):
        self.get_field(field_name).set_python(value)

    def __getitem__(self, field_name):
        return self.get_field(field_name).get_python()

    def __delitem__(self, field_name):
        self[field_name] = None

    def __iter__(self):
        for field_name, field in six.iteritems(self._fields):
            yield field_name, field.get_python()

    def __hash__(self):
        return hash((self.id, self.app))

    def __lt__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError("Comparisons not supported between instances of '{}' and '{}'".format(
                other.__class__.__name__,
                self.__class__.__name__
            ))

        tracking_number_self = int(self.tracking_id.split('-')[1])
        tracking_number_other = int(other.tracking_id.split('-')[1])

        return (self.app.name, tracking_number_self) < (other.app.name, tracking_number_other)

    def __premap_fields(self):
        """Build field instances using field definitions in app manifest
        
        Map raw record field data into appropriate field instances with their correct respective types
        """
        # Circular imports
        from swimlane.core.fields import resolve_field_class

        for field_definition in self.app._raw['fields']:
            field_class = resolve_field_class(field_definition)

            field_instance = field_class(field_definition['name'], self)
            value = self._raw['values'].get(field_instance.id)
            field_instance.set_swimlane(value)

            self._fields[field_instance.name] = field_instance

    def get_cache_index_keys(self):
        """Return values available for retrieving records, but only for already existing records"""
        if not (self.id and self.tracking_id):
            raise NotImplementedError

        return {
            'id': self.id,
            'tracking_id': self.tracking_id
        }

    def get_field(self, field_name):
        """Get field instance used to get, set, and serialize internal field value

        Args:
            field_name (str): Field name or key to retrieve

        Returns:
            Field: Requested field instance

        Raises:
             UnknownField: Raised if `field_name` not found in parent App
        """
        try:
            return self._fields[self.app.resolve_field_name(field_name)]
        except KeyError:
            raise UnknownField(self.app, field_name, self._fields.keys())

    def validate(self):
        """Explicitly validate field data

        Notes:
            Called automatically during save call before sending data to server

        Raises:
             ValidationError: If any fields fail validation
        """
        for field in (_field for _field in six.itervalues(self._fields) if _field.required):
            if field.get_swimlane() is None:
                raise ValidationError(self, 'Required field "{}" is not set'.format(field.name))

    def save(self):
        """Persist record changes on Swimlane server
        
        Updates internal raw data with response content from server to guarantee calculated field values match values on
        server
        
        Raises:
            ValidationError: If any fields fail validation
        """

        if self.is_new:
            method = 'post'
        else:
            method = 'put'

        # Pop off fields with None value to allow for saving empty fields
        copy_raw = copy.copy(self._raw)
        values_dict = {}
        for key, value in six.iteritems(copy_raw['values']):
            if value is not None:
                values_dict[key] = value
        copy_raw['values'] = values_dict

        self.validate()

        response = self._swimlane.request(
            method,
            'app/{}/record'.format(self.app.id),
            json=copy_raw
        )

        # Reinitialize record with new raw content returned from server to update any calculated fields
        self.__init__(self.app, response.json())

        # Manually cache self after save to keep cache updated with latest data
        self._swimlane.resources_cache.cache(self)

    def delete(self):
        """Delete record from Swimlane server

        .. versionadded:: 2.16.1

        Resets to new state, but leaves field data as-is. Saving a deleted record will create a new Swimlane record

        Raises
            ValueError: If record.is_new
        """
        if self.is_new:
            raise ValueError('Cannot delete a new Record')

        self._swimlane.request(
            'delete',
            'app/{}/record/{}'.format(self.app.id, self.id)
        )

        del self._swimlane.resources_cache[self]

        # Modify current raw values indicating an unsaved record but persisting field data
        raw = copy.deepcopy(self._raw)
        raw['id'] = None
        raw['isNew'] = True

        self.__init__(self.app, raw)

    @property
    def restrictions(self):
        """Returns cached set of retrieved UserGroups in the record's list of allowed accounts"""
        return [UserGroup(self._swimlane, raw) for raw in self._raw['allowed']]

    def add_restriction(self, *usergroups):
        """Add UserGroup(s) to list of accounts with access to record

        .. versionadded:: 2.16.1

        UserGroups already in the restricted list can be added multiple times and duplicates will be ignored

        Notes:
            Does not take effect until calling `record.save()`

        Args:
            *usergroups (UserGroup): 1 or more Swimlane UserGroup(s) to add to restriction list

        Raises:
            TypeError: If 0 UserGroups provided or provided a non-UserGroup instance
        """
        if not usergroups:
            raise TypeError('Must provide at least one UserGroup for restriction')

        allowed = copy.copy(self._raw.get('allowed', []))

        for usergroup in usergroups:
            if not isinstance(usergroup, UserGroup):
                raise TypeError('Expected UserGroup, received `{}` instead'.format(usergroup))

            selection = usergroup.as_usergroup_selection()
            if selection not in allowed:
                allowed.append(selection)

        self._raw['allowed'] = allowed

    def remove_restriction(self, *usergroups):
        """Remove UserGroup(s) from list of accounts with access to record

        .. versionadded:: 2.16.1

        Notes:
            Does not take effect until calling `record.save()`

        Warnings:
            Providing no UserGroups will clear the restriction list, opening access to ALL accounts

        Args:
            *usergroups (UserGroup): 0 or more Swimlane UserGroup(s) to remove from restriction list

        Raises:
            TypeError: If provided a non-UserGroup instance
            ValueError: If provided UserGroup not in current restriction list
        """
        if usergroups:
            allowed = copy.copy(self._raw.get('allowed', []))

            for usergroup in usergroups:
                if not isinstance(usergroup, UserGroup):
                    raise TypeError('Expected UserGroup, received `{}` instead'.format(usergroup))
                try:
                    allowed.remove(usergroup.as_usergroup_selection())
                except ValueError:
                    raise ValueError('UserGroup `{}` not in record `{}` restriction list'.format(usergroup, self))
        else:
            allowed = []

        self._raw['allowed'] = allowed


def record_factory(app, fields=None):
    """Return a temporary Record instance to be used for field validation and value parsing

    Args:
        app (App): Target App to create a transient Record instance for
        fields (dict): Optional dict of fields and values to set on new Record instance before returning

    Returns:
        Record: Unsaved Record instance to be used for validation, creation, etc.
    """
    # pylint: disable=line-too-long
    record = Record(app, {
        '$type': Record._type,
        'isNew': True,
        'applicationId': app.id,
        'comments': {
            '$type': 'System.Collections.Generic.Dictionary`2[[System.String, mscorlib],[System.Collections.Generic.List`1[[Core.Models.Record.Comments, Core]], mscorlib]], mscorlib'
        },
        'values': {
            '$type': 'System.Collections.Generic.Dictionary`2[[System.String, mscorlib],[System.Object, mscorlib]], mscorlib'
        }
    })

    fields = fields or {}

    for name, value in six.iteritems(fields):
        record[name] = value

    # Pop off fields with None value to allow for saving empty fields
    copy_raw = copy.copy(record._raw)
    values_dict = {}
    for key, value in six.iteritems(copy_raw['values']):
        if value is not None:
            values_dict[key] = value
    record._raw['values'] = values_dict

    return record
