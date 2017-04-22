import pendulum

from swimlane.core.resources import APIResource, UserGroup
from .base import FieldCursor, ReadOnly, CursorField


class CommentCursor(FieldCursor):
    """Returned by CommentField to allow iteration and creation of Comment instances"""


class Comment(APIResource):
    """Abstraction of a single comment from a comment field"""

    def __init__(self, swimlane, raw):
        super(Comment, self).__init__(swimlane, raw)

        self.user = UserGroup(swimlane, self._raw['createdByUser'])
        self.created_date = pendulum.parse(self._raw['createdDate'])
        self.message = self._raw['message']

    def __str__(self):
        return self.message


class CommentsField(ReadOnly, CursorField):

    field_type = 'Core.Models.Fields.CommentsField, Core'
    cursor_class = CommentCursor

    def get_initial_elements(self):
        raw_comments = self.record._raw['comments'].get(self.id, [])

        return [Comment(self.record._swimlane, raw) for raw in raw_comments]
