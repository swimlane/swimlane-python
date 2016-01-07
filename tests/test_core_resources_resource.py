from pytest import raises

from swimlane.core.resources import Resource


class Foo(Resource):
    def __init__(self, fields):
        super(Foo, self).__init__(fields)
        self.baz = "baz"

    def bar(self):
        return "bar"


def test_custom_get_attr():
    foo = Foo({"a": 1, "b": 2})
    assert foo
    assert foo.bar() == "bar"
    assert foo.baz == "baz"
    assert foo.a == 1
    assert foo.b == 2
    with raises(AttributeError):
        foo.doesnt_exist

    foo.a = 3
    assert foo._fields["a"] == 3
