import pendulum

from swimlane.core.resources.base import APIResource
from swimlane.core.resources.usergroup import UserGroup


class Comment(APIResource):
    """Abstraction of a single comment from a comment field

    Attributes:
        user (UserGroup): UserGroup instance of user who created the comment
        created_date (pendulum.DateTime): Pendulum datetime of when comment was created
        message (str): Comment message body
    """

    def __init__(self, swimlane, raw):
        super(Comment, self).__init__(swimlane, raw)

        self.user = UserGroup(swimlane, self._raw['createdByUser'])
        self.created_date = pendulum.parse(self._raw['createdDate'])
        self.message = self._raw['message']
        self.is_rich_text = self._raw.get('isRichText', False)

    def __str__(self):
        return self.message

    def for_json(self):
        """Called by CommentField.for_json(), returns relevant Comment attributes in JSON-compatible format"""
        return {
            'message': self.message,
            'createdDate': self._raw['createdDate'],
            'createdByUser': self.user.for_json()
        }
