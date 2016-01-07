from swimlane.core.resources import Group

GROUP_ID = "568496a855d95f26400864bb"


def test_find_all(default_client):
    groups = list(Group.find_all())
    assert len(groups) > 0


def test_find_by_id(default_client):
    group = Group.find(group_id=GROUP_ID)
    assert group
    assert not group.disabled
    assert group.name == "Empty"


def test_find_by_name(default_client):
    groups = list(Group.find(name="Private"))
    assert groups
    assert len(groups) == 1
    pis = groups[0]
    assert pis
    assert not pis.disabled
    assert pis.name == "Private Eyes"


def test_find_multiple_by_name(default_client):
    groups = list(Group.find(name="E"))
    assert len(groups) == 2
