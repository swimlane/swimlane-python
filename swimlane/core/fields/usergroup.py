from swimlane.core.resources.usergroup import UserGroup
from .base import MultiSelectField


class UserGroupField(MultiSelectField):
    """Manages getting/setting users from record User/Group fields"""

    field_type = 'Core.Models.Fields.UserGroupField, Core'

    supported_types = [UserGroup]

    def set_swimlane(self, value):
        """Workaround for reports returning an empty usergroup field as a single element list with no id/name"""
        if value == [{"$type": "Core.Models.Utilities.UserGroupSelection, Core"}]:
            value = []

        return super(UserGroupField, self).set_swimlane(value)

    def cast_to_python(self, value):
        """Convert JSON definition to UserGroup object"""
        # v2.x does not provide a distinction between users and groups at the field selection level, can only return
        # UserGroup instances instead of specific User or Group instances
        if value is not None:
            value = UserGroup(self.record._swimlane, value)

        return value

    def cast_to_swimlane(self, value):
        """Dump UserGroup back to JSON representation"""
        if value is not None:
            value = value.get_usergroup_selection()

        return value
