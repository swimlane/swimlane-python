import pendulum

from swimlane.core.resources import APIResource, UserGroup
from .base import CursorField, FieldCursor, ReadOnly


class Comment(APIResource):
    """Abstraction of a single comment from a comment field"""

    def __init__(self, swimlane, raw):
        super(Comment, self).__init__(swimlane, raw)

        self.user = UserGroup(swimlane, self._raw['createdByUser'])
        self.created_date = pendulum.parse(self._raw['createdDate'])
        self.message = self._raw['message']

    def __str__(self):
        return self.message


class CommentCursor(FieldCursor):
    """Returned by CommentField to allow iteration and creation of Comment instances"""

    def comment(self, message):
        """Add new comment to record comment field"""
        message = str(message)

        sw_repr = {
            '$type': 'Core.Models.Record.Comments, Core',
            'createdByUser': self._record._swimlane.user.get_usergroup_selection(),
            'createdDate': pendulum.now().to_rfc3339_string(),
            'message': message
        }

        comment = Comment(self._swimlane, sw_repr)
        self._elements.append(comment)

        self._record._raw['comments'].setdefault(self._field.id, [])
        self._record._raw['comments'][self._field.id].append(comment._raw)

        return comment


class CommentsField(ReadOnly, CursorField):

    field_type = 'Core.Models.Fields.CommentsField, Core'
    cursor_class = CommentCursor

    def get_initial_elements(self):
        raw_comments = self.record._raw['comments'].get(self.id, [])

        return [Comment(self.record._swimlane, raw) for raw in raw_comments]
