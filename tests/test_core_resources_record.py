from swimlane.core.resources import Record, App

APP_ID = "567490ad55d95d5c30d02266"
RECORD_ID = "567490e955d95d5c30d022bf"
USER_ID = "5674909d55d95d5c30d02200"


def test_new_for(default_client):
    assert Record.new_for(APP_ID)


def test_find(default_client):
    assert Record.find(APP_ID, RECORD_ID)


def test_insert(default_client):
    record = Record.new_for(APP_ID)
    assert record.isNew
    record.values["foo"] = "123456"
    record.insert()
    assert not record.isNew


def test_update(default_client):
    record = Record.new_for(APP_ID)
    record.values["foo"] = "123456"
    record.insert()
    assert not record.isNew
    record.values["foo"] = "abcdef"
    record.update()


def test_add_comment(default_client):
    app = App.find(app_id=APP_ID)
    field_id = app.field_id("One")
    record = Record.new_for(APP_ID)
    record.values[field_id] = "abc123"
    record.insert()

    assert len(record.comments) == 1

    record.add_comment(field_id, USER_ID, "A test comment")

    record = Record.find(APP_ID, record.id)
    assert len(record.comments) == 2


def test_references(default_client):
    app_ref_id = "56881bd655d95d4e00871284"
    rec_id = "568825cb55d95d2a005f2ef7"
    remote_rec_id = "568825d555d95d2a005f2f11"
    remote_field_id = "56881c1c848714d8b6d70683"
    field_id = "567490b554929bf5dbe7021e"

    record = Record.find(APP_ID, rec_id)
    refs = record.references(field_id, [remote_rec_id], [remote_field_id])
    ref_rec = list(refs)[0]
    assert ref_rec.values[remote_field_id][0] == rec_id
