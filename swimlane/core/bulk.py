"""Helpers for bulk methods"""


class _BulkModificationOperation(object):
    """Base class for bulk_modify value modification operators

    Acts as container to wrap the modification type with the target value for the bulk operation

    Examples:

        swimlane.records.bulk_modify(
            record,
            values={
                'Field A': 'new value',
                'Field B': Append('new value'),
                'Field C': Clear(),
                ...
            }
        )
    """

    type = None

    def __init__(self, value):
        self.value = value


class Replace(_BulkModificationOperation):
    """Bulk modification 'Replace with'/'Replace all with' operation"""
    type = 'create'


class Clear(_BulkModificationOperation):
    """Bulk modification 'Clear field' operation"""
    type = 'delete'

    def __init__(self):
        super(Clear, self).__init__(None)


class Append(_BulkModificationOperation):
    """Bulk modification 'Add to existing' operation"""
    type = 'append'


class Remove(_BulkModificationOperation):
    """Bulk modification 'Find and remove these' operation"""
    type = 'subtract'
