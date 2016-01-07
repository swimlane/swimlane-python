from swimlane.core.resources import App

ID = "567490ad55d95d5c30d02266"
NAME = "Incident Response"
ACRONYM = "IR"


def test_find_all_applications(default_client):
    assert len(list(App.find_all())) > 0


def test_find_application_by_id(default_client):
    assert App.find(app_id=ID).name == NAME


def test_find_application_by_name(default_client):
    assert App.find(name=NAME).name == NAME


def test_find_application_by_acronym(default_client):
    assert App.find(acronym=ACRONYM).name == NAME


def test_find_nothing(default_client):
    assert App.find(acronym="") is None


def test_field_id(default_client):
    app = App.find(app_id=ID)
    assert app.field_id("One")
    assert not app.field_id("WONTFINDME")
