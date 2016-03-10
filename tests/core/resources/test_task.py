from swimlane.core.resources import Task, App, Record

APP_ID = "567490ad55d95d5c30d02266"


def test_find_all(default_client):
    assert len(list(Task.find_all())) == 2


def test_find_by_name(default_client):
    assert Task.find(name="Print some stuff")


def test_run(default_client):
    task = Task.find(name="Print some stuff")
    record = Record.new_for(APP_ID)
    record.insert()
    task.run(record=record)

