import weakref

import six

from swimlane.core.resources import Record
from swimlane.core.resolver import SwimlaneResolver
from swimlane.utils import random_string


class RecordAdapter(SwimlaneResolver):
    """Allows retrieval and creation of Swimlane records"""

    def __init__(self, app):
        super(RecordAdapter, self).__init__(app._swimlane)

        self.__ref_app = weakref.ref(app)

    @property
    def _app(self):
        """Resolve app weak reference"""
        return self.__ref_app()

    def get(self, **kwargs):
        """Get a single record by full id"""
        record_id = kwargs.pop('id', None)

        if kwargs:
            raise TypeError('Unexpected arguments: {}'.format(kwargs))

        if record_id is None:
            raise TypeError('Must provide id argument')

        response = self._swimlane.request('get', "app/{0}/record/{1}".format(self._app.id, record_id))

        return Record(self._app, response.json())

    def search(self, *filter_tuples):
        """Shortcut to generate a new temporary search report using provided filters and return the results"""
        report = self._app.reports.build('search-' + random_string(8))

        for filter_tuple in filter_tuples:
            report.filter(*filter_tuple)

        return list(report)

    def create(self, **fields):
        """Create and return a new record in associated app and return the corresponding Record instance
        
        Arguments should be field names with their respective python values
        """
        # Use temporary Record instance to build fields and inject python values
        #pylint: disable=line-too-long
        new_record = Record(self._app, {
            '$type': Record._type,
            'isNew': True,
            'applicationId': self._app.id,
            'comments': {
                '$type': 'System.Collections.Generic.Dictionary`2[[System.String, mscorlib],[System.Collections.Generic.List`1[[Core.Models.Record.Comments, Core]], mscorlib]], mscorlib'
            },
            'values': {
                '$type': 'System.Collections.Generic.Dictionary`2[[System.String, mscorlib],[System.Object, mscorlib]], mscorlib'
            }
        })

        for field_name, field_value in six.iteritems(fields):
            new_record[field_name] = field_value

        # Send converted data to server
        response = self._swimlane.request(
            'post',
            'app/{}/record'.format(self._app.id),
            data=new_record.serialize()
        )

        # Return new Record instance from returned data
        return Record(self._app, response.json())
