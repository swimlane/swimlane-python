import pytest
from swimlane.exceptions import SwimlaneException

@pytest.fixture(autouse=True, name='app', scope='module')
def my_fixture(helpers):
    # setup stuff
    helpers.import_content('basic_task_app.ssp')
    yield helpers.swimlane_instance.apps.get(name='Basic Task App')
    # teardown stuff
    helpers.cleanupData()


def test_execute_task(app):
    # sample_task has input 'Single-line text field' and ouput 'Text List'.
    # Task splits input into a list and sends to output.
    record = app.records.create()
    record["Single-line text field"] = "Testing 12345"
    record.execute_task("sample_task")  
    assert record['Text List'][0] == 'Testing'
    assert record['Text List'][1] == '12345'
    record.delete()


def test_execute_task_raises(app):
    record = app.records.create()
    record["Single-line text field"] = "Testing 12345"
    with pytest.raises(SwimlaneException):
        # Test that a failed task raises an exception.
        record.execute_task("failed_task")
    record.delete()
