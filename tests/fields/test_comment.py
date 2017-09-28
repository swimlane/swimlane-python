from datetime import datetime

import mock

from swimlane.core.fields.comment import CommentCursor
from swimlane.core.resources.comment import Comment
from swimlane.core.resources.usergroup import UserGroup


def test_comment_field(mock_record, mock_swimlane):
    # CommentsField
    # Cursor managing iteration and addition of comments
    # Automatically added to record during save without manual call to create comment
    comments = mock_record['Investigation Summary']
    assert isinstance(comments, CommentCursor)
    assert len(comments) == 1

    for comment in comments:
        assert isinstance(comment, Comment)
        assert isinstance(comment.message, str)
        assert str(comment) == comment.message
        assert isinstance(comment.user, UserGroup)
        assert isinstance(comment.created_date, datetime)

    # Add new comment
    with mock.patch.object(mock_swimlane._session, 'request') as mock_request:
        mock_response = mock.MagicMock()
        mock_response.json.return_value = [{
            '$type': 'Core.Models.Identity.ApplicationUser, Core',
            'active': False,
            'createdByUser': {'$type': 'Core.Models.Utilities.UserGroupSelection, Core'},
            'createdDate': '2017-03-31T09:10:52.717Z',
            'disabled': False,
            'displayName': 'admin',
            'groups': [],
            'id': '58de1d1c07637a0264c0ca6a',
            'isAdmin': True,
            'isMe': False,
            'lastLogin': '2017-04-27T14:11:38.54Z',
            'lastPasswordChangedDate': '2017-03-31T09:10:52.536Z',
            'modifiedByUser': {'$type': 'Core.Models.Utilities.UserGroupSelection, Core'},
            'modifiedDate': '2017-03-31T09:10:52.76Z',
            'name': 'admin',
            'passwordComplexityScore': 3,
            'passwordHash': 'AQAAAAEAACcQAAAAEESp9LR0jN3qPF2fw5qWdyceYxbeBbawMW5AFt31dA5n3xX16MFJWsU/j82heenFww==',
            'passwordResetRequired': False,
            'roles': [],
            'userName': 'admin'}]

        mock_request.return_value = mock_response

        comments.comment('New comment message')

        # Not persisted until saved, but still listed on local record
        assert len(comments) == 2
        assert comments[1].message == 'New comment message'
