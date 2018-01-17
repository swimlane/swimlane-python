import pendulum

from swimlane.core.resources.comment import Comment
from .base import CursorField, FieldCursor, ReadOnly


class CommentCursor(FieldCursor):
    """Returned by CommentField to allow iteration and creation of Comment instances"""

    def comment(self, message):
        """Add new comment to record comment field"""
        message = str(message)

        sw_repr = {
            '$type': 'Core.Models.Record.Comments, Core',
            'createdByUser': self._record._swimlane.user.as_usergroup_selection(),
            'createdDate': pendulum.now().to_rfc3339_string(),
            'message': message
        }

        comment = Comment(self._swimlane, sw_repr)
        self._elements.append(comment)

        self._record._raw['comments'].setdefault(self._field.id, [])
        self._record._raw['comments'][self._field.id].append(comment._raw)

        return comment


class CommentsField(ReadOnly, CursorField):

    field_type = (
        'Core.Models.Fields.CommentsField, Core',
        'Core.Models.Fields.Comments.CommentsField, Core'
    )
    cursor_class = CommentCursor
    bulk_modify_support = False

    def get_initial_elements(self):
        raw_comments = self.record._raw['comments'].get(self.id, [])

        return [Comment(self.record._swimlane, raw) for raw in raw_comments]
