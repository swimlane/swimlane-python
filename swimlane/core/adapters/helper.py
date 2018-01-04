import pendulum

from swimlane.core.resolver import SwimlaneResolver
from swimlane.utils.version import requires_swimlane_version


class HelperAdapter(SwimlaneResolver):
    """Adapter providing any miscellaneous API calls not better suited for another adapter"""

    @requires_swimlane_version('2.15')
    def add_record_references(self, app_id, record_id, field_id, target_record_ids):
        """Bulk operation to directly add record references without making any additional requests

        Warnings:
            Does not perform any app, record, or target app/record validation

        Args:
            app_id (str): Full App ID string
            record_id (str): Full parent Record ID string
            field_id (str): Full field ID to target reference field on parent Record string
            target_record_ids (List(str)): List of full target reference Record ID strings
        """

        self._swimlane.request(
            'post',
            'app/{0}/record/{1}/add-references'.format(app_id, record_id),
            json={
                'fieldId': field_id,
                'targetRecordIds': target_record_ids
            }
        )

    def add_comment(self, app_id, record_id, field_id, message):
        """Directly add a comment to a record without retrieving the app or record first

        Warnings:
            Does not perform any app, record, or field ID validation

        Args:
            app_id (str): Full App ID string
            record_id (str): Full parent Record ID string
            field_id (str): Full field ID to target reference field on parent Record string
            message (str): New comment message body
        """

        self._swimlane.request(
            'post',
            'app/{0}/record/{1}/{2}/comment'.format(
                app_id,
                record_id,
                field_id
            ),
            json={
                'message': message,
                'createdDate': pendulum.now().to_rfc3339_string()
            }
        )

    def check_bulk_job_status(self, job_id):
        """Check status of bulk_delete or bulk_modify jobs
        .. versionadded:: 2.17.0
        Args:
            job_id (str): Job ID

        Returns:
            :class:`list` of :class:`dict`: List of dictionaries containing job history

        """

        return self._swimlane.request('get', "logging/job/{0}".format(job_id)).json()

