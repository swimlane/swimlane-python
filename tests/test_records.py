from swimlane.core.auth import Client
from swimlane.records import add_references


def test_add_references():
    Client.set_default(server", "usr", "pwd", False)

    print add_references(
        record_id="5670dcec0e23ab0e4c363e12",
        keywords="chisrv7008",
        app_acronym="SOC",
        remote_app_acronym="CMDB",
        field_name="CMDB"
    )
