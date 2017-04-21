import pendulum

from swimlane.core.resources import APIResource, UserGroup
from .base import FieldCursor, ReadOnly, CursorField


class CommentCursor(FieldCursor):
    """Returned by CommentField to allow iteration and creation of Comment instances"""

    def __init__(self, field):
        super(CommentCursor, self).__init__(field)

        raw_comments = field.record._raw['comments'].get(field.id, [])

        self._elements = [Comment(self._swimlane, raw) for raw in raw_comments]


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

    _field_type = 'Core.Models.Fields.CommentsField, Core'
    cursor_class = CommentCursor


