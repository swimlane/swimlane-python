from swimlane.core.resources.usergroup import UserGroup, User
from swimlane.exceptions import ValidationError
from .base import MultiSelectField


class UserGroupField(MultiSelectField):
    """Manages getting/setting users from record User/Group fields"""

    field_type = (
        'Core.Models.Fields.UserGroupField, Core',
        'Core.Models.Fields.UserGroup.UserGroupField, Core'
    )

    supported_types = [UserGroup]

    def __init__(self, *args, **kwargs):
        super(UserGroupField, self).__init__(*args, **kwargs)

        members = self.field_definition.get('members', [])

        self._allowed_user_ids = set([r['id'] for r in members if r['selectionType'] == 'users'])
        self._allowed_member_ids = set([r['id'] for r in members if r['selectionType'] == 'members'])

        self._allowed_group_ids = set([r['id'] for r in members if r['selectionType'] == 'groups'])
        self._allowed_subgroup_ids = set([r['id'] for r in members if r['selectionType'] == 'subGroups'])

        self._show_all_users = self.field_definition['showAllUsers']
        self._show_all_groups = self.field_definition['showAllGroups']

    def validate_value(self, value):
        """Validate new user/group value against any User/Group restrictions

        Attempts to resolve generic UserGroup instances if necessary to respect special "Everyone" group, and
        "All Users" + "All Groups" options
        """
        super(UserGroupField, self).validate_value(value)

        if value is not None:
            # Ignore validation if all users + groups are allowed
            if self._show_all_groups and self._show_all_users:
                return

            # Try to directly check allowed ids against user/group id first to avoid having to resolve generic
            # UserGroup with an additional request
            if value.id in self._allowed_user_ids | self._allowed_group_ids:
                return

            # Resolve to check Users vs Groups separately
            value = value.resolve()

            if isinstance(value, User):
                self._validate_user(value)
            else:
                self._validate_group(value)

    def _validate_user(self, user):
        """Validate a User instance against allowed user IDs or membership in a group"""
        # All users allowed
        if self._show_all_users:
            return

        # User specifically allowed
        if user.id in self._allowed_user_ids:
            return

        # User allowed by group membership
        user_member_group_ids = set([g['id'] for g in user._raw['groups']])
        if user_member_group_ids & self._allowed_member_ids:
            return

        raise ValidationError(
            self.record,
            'User `{}` is not a valid selection for field `{}`'.format(
                user,
                self.name
            )
        )

    def _validate_group(self, group):
        """Validate a Group instance against allowed group IDs or subgroup of a parent group"""
        # All groups allowed
        if self._show_all_groups:
            return

        # Group specifically allowed
        if group.id in self._allowed_group_ids:
            return

        # Group allowed by subgroup membership
        for parent_group_id in self._allowed_subgroup_ids:
            # Get each group, and check subgroup ids
            parent_group = self._swimlane.groups.get(id=parent_group_id)
            parent_group_child_ids = set([g['id'] for g in parent_group._raw['groups']])
            if group.id in parent_group_child_ids:
                return

        raise ValidationError(
            self.record,
            'Group `{}` is not a valid selection for field `{}`'.format(
                group,
                self.name
            )
        )

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
            value = UserGroup(self._swimlane, value)

        return value

    def cast_to_swimlane(self, value):
        """Dump UserGroup back to JSON representation"""
        if value is not None:
            value = value.as_usergroup_selection()

        return value
