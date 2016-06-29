"""Provides a Record class."""

from datetime import datetime
from warnings import warn

from ..auth import Client
from .group import Group
from .resource import Resource
from .user import User


class Record(Resource):
    """A simple abstraction over a Swimlane record resource."""

    def __init__(self, fields):
        """Init a Record with fields.

        Args:
            fields (dict): A dict of fields and values
        """
        super(Record, self).__init__(fields)

    def insert(self):
        """Insert the current record."""
        warn(
            'Record.insert method will be deleted in v0.1.0, use Record.save',
            category=DeprecationWarning)
        self.save()

    def update(self):
        """Update the current record."""
        warn(
            'Record.update method will be deleted in v0.1.0, use Record.save',
            category=DeprecationWarning)
        self.save()

    def save(self):
        """Create/update a record."""
        if not hasattr(self, 'isNew') or self.isNew is True:
            self._fields = Client.post(
                self, "app/{0}/record".format(self.applicationId))
        else:
            self._fields = Client.put(
                self, "app/{0}/record".format(self.applicationId))

    def reload(self):
        """Reload a record instance."""
        if not hasattr(self, 'isNew') or self.isNew is True:
            raise Exception(
                'Cannot reload an unsaved record, call save() first')
        r = Record.find(self.applicationId, self.id)
        self._fields.update(**r._fields)

    def add_comment(self, field_id, user_id, message):
        """Add a comment to a field.

        Args:
            field_id (str): The field ID.
            user_id (str): The user ID of the commenting user.
            message (str): The comment message.
        """
        Client.post({
            "message": message,
            "createdDate": datetime.utcnow().isoformat() + "Z",
            "createdByUser": user_id
        }, "app/{0}/record/{1}/{2}/comment".format(
            self.applicationId, self.id, field_id))

    def references(self, field_id, record_ids, ref_field_ids):
        """Get referenced Records.

        Args:
            field_id (str): The ID of the field on the current record.
            record_ids (list): The IDs of any records to retrieve.
            field_ids (list): The IDs of any fields to retrieve.

        Returns:
            A generator that yields all referenced Records.
        """
        url = ("app/{0}/record/{1}/references"
               "?recordIds={2}&fieldIds={3}".format(
                   self.applicationId, self.id,
                   ",".join(record_ids),
                   ",".join(ref_field_ids)))
        return (Record(r) for r in Client.get(url))

    @classmethod
    def new_for(cls, app_id):
        """Get a prefilled Record for the App designated by app_id.

        Args:
            app_id (str): A valid App ID.

        Return:
            A dict containing default fields and values for a Record.
        """
        return Record(Client.get("app/{0}/record".format(app_id)))

    @classmethod
    def find(cls, app_id, record_id):
        """Find a Record by app_id and record_id.

        Args:
            app_id (str): A valid App ID
            record_id (str): A valid Record ID

        Return:
            A Record
        """
        return Record(Client.get("app/{0}/record/{1}".format(app_id,
                                                             record_id)))

    def restrict(self, *user_groups, **kwargs):
        """
        Restrict the record to specific users and/or groups.

        :param user_groups: One or more User/Group instances.
        :type user_groups: :class:`Group` or :class:`User`
        :param append: Append users/groups to existing restriction.
        :type append: bool
        """
        allowed = [ug.summary for ug in user_groups
                   if isinstance(ug, (Group, User))]
        if 'append' in kwargs and kwargs['append']:
            allowed = self.allowed + allowed
        Client.put(allowed, 'app/{0}/record/{1}/restrict'.format(
            self.applicationId, self.id))
        return allowed
