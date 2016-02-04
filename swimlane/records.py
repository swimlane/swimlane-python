"""This module provides functions that are useful for working with records."""

from .core.auth import Client
from .core.resources import App, Record, Report, User
from .core.search import Search


def add_references(record_id,
                   keywords,
                   app_id=None,
                   app_name=None,
                   remote_app_id=None,
                   remote_app_name=None,
                   field_id=None,
                   field_name=None):
    """Add references to a record by querying with keywords.

    This function creates references on a record in one app to records in
    another app. Note that you can specify the apps by ID, name, or acronym and
    you can specify the reference field by ID or name.

    Args:
        record_id (str): The ID of the record references will be added to.
        keywords (str): The keywords that will be used to search for records.
        app_id (str): An App ID.
        app_name (str): An App name.
        remote_app_id (str): The ID of the App to query against.
        remote_app_name (str): The name of the App to query against.
        field_id (str): The field ID that references will be added to.
        field_name (str): The field name that references will be added to.

    Returns:
        A list of the Records that were referenced.
    """
    app = App.find(app_id=app_id, name=app_name)

    if not app:
        raise Exception("Unable to find App")

    if not field_id and field_name:
        field_id = app.field_id(field_name)
    if not field_id:
        raise Exception("field_id or field_name must be supplied")

    remote_app = App.find(app_id=remote_app_id, name=remote_app_name)

    if not remote_app:
        raise Exception("Unable to find remote App")

    current_user = next(User.find(name=Client.default.username), None)

    report = Report.new_for(remote_app.id, current_user.id, "addrefs")
    report.keywords = keywords

    records = Search(report).execute().records

    if records:
        record = Record.find(app.id, record_id)
        if not record:
            raise Exception("Unable to find record")
        record.values[field_id] = [r.id for r in records]
        record.update()

    return records
