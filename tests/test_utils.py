import os
import string
import sys

import mock
import pytest
from pkg_resources import DistributionNotFound

from swimlane.core.resolver import SwimlaneResolver
from swimlane.exceptions import InvalidSwimlaneBuildVersion
from swimlane.utils import (
    random_string,
    get_recursive_subclasses,
    import_submodules,
    one_of_keyword_only
)
from swimlane.utils.version import (
    compare_versions,
    requires_swimlane_version,
    get_package_version
)


def test_random_string():
    generated_string = random_string(8)
    assert len(generated_string) == 8
    assert set(generated_string).issubset(set(string.ascii_letters + string.digits))

    generated_string = random_string(20, string.ascii_uppercase)
    assert len(generated_string) == 20
    assert set(generated_string).issubset(set(string.ascii_uppercase))


def test_get_recursive_subclasses():
    class Base(object):
        pass

    class DirectChild(Base):
        pass

    class IndirectChild(DirectChild):
        pass

    assert sorted([DirectChild, IndirectChild], key=lambda cls: cls.__name__) == sorted(get_recursive_subclasses(Base), key=lambda cls: cls.__name__)
    assert [IndirectChild] == get_recursive_subclasses(DirectChild)


def test_import_submodules():
    fixture_path = os.path.join(
        os.path.dirname(__file__),
        'fixtures'
    )
    sys.path.insert(0, fixture_path)

    imported_modules = import_submodules('import_pkg')
    assert len(imported_modules) == 2

    sample_module = imported_modules['import_pkg.sample_module']
    assert sample_module.fixture_value == 'fixture_value'

    sys.path.pop(0)


@pytest.mark.parametrize('inputs,expected', [
    ('2', 0),
    ('1', 1),
    ('3', -1),
    ('2.13', 0),
    ('2.12', 1),
    ('2.14', -1),
    ('2.13.3', -1),
    ('2.13.2', 0),
    ('2.13.2-173414', 0),
    ('2.13.2-173415', -1)
])
def test_compare_versions_no_zerofill(inputs, expected):
    """Test compare versions when only comparing sections of version included in both provided versions"""
    assert compare_versions(inputs, '2.13.2-173414') == expected


@pytest.mark.parametrize('inputs,expected', [
    ('2', 1),
    ('1', 1),
    ('3', -1),
    ('2.13', 1),
    ('2.12', 1),
    ('2.14', -1),
    ('2.13.3', -1),
    ('2.13.2', 1),
    ('2.13.2-173414', 0),
    ('2.13.2-173415', -1)
])
def test_compare_versions_with_zerofill(inputs, expected):
    """Test compare versions when comparing sections of version with default 0 for missing sections"""
    target = '2.13.2-173414'
    assert compare_versions(inputs, target, True) == expected
    assert compare_versions(target, inputs, True) == -expected


def test_get_package_version():
    mock_dist = mock.MagicMock()
    mock_dist.version = '1.2.3'

    with mock.patch('swimlane.utils.version.get_distribution', return_value=mock_dist):
        version = get_package_version()
        assert tuple(version.split('.')[:2]) > ('0', '0', '0')

    with mock.patch('swimlane.utils.version.get_distribution', side_effect=DistributionNotFound):
        assert get_package_version() == '0.0.0.dev'


@pytest.mark.parametrize('kwargs,expected', [
    [
        {},
        TypeError
    ],
    [
        {'a': 'a', 'b': 'b'},
        TypeError
    ],
    [
        {'other': 'value'},
        TypeError
    ],
    [
        {'a': 'value_a'},
        'value_a'
    ],
    [
        {'b': 'value_b'},
        'value_b'
    ]
])
def test_one_of_keyword_only(kwargs, expected):
    """Test decorator requires exactly one keyword argument from provided list of options"""

    valid_options = ('a', 'b')

    @one_of_keyword_only(*valid_options)
    def func(key, value):
        return key in valid_options and value == expected

    if expected is TypeError:
        with pytest.raises(expected):
            func(**kwargs)

    else:
        assert func(**kwargs)


class TestRequiresSwimlaneVersion(object):
    """Tests for the requires_swimlane_version decorator"""

    def _get_resolver(self, min_version, max_version):
        """Factory used in tests"""
        class TestResolver(SwimlaneResolver):
            @requires_swimlane_version(min_version, max_version)
            def func(self, *args, **kwargs):
                return args, kwargs

        return TestResolver

    @pytest.mark.parametrize('min_version,max_version', [
        ('2.13', '2.12'),
        ('2', '1.2.3'),
        (None, None)
    ])
    def test_invalid_version_range(self, min_version, max_version):
        """Test that requires_swimlane_version raises ValueError when receiving conflicting version range"""
        with pytest.raises(ValueError):
            self._get_resolver(min_version, max_version)

    @pytest.mark.parametrize('min_version,max_version', [
        ('2.13', '2.13'),
        ('2.12', '2.13'),
        (None, '2.13'),
        ('2.13', None),
        ('2', '3.2.1'),
        ('2.3.4', '3')
    ])
    def test_valid_version_range(self, min_version, max_version):
        """Test that requires_swimlane_version does not raise exceptions when given a valid version range"""
        self._get_resolver(min_version, max_version)

    @pytest.mark.parametrize('swimlane_version,min_version,max_version', [
        ('2.13', '2.14', None),
        ('2.13.2', '2.14', None),
        ('2.13.2', '2.13.3', None),
        ('2.13', None, '2.12'),
        ('2.13.2', None, '2.13'),
        ('2.13.2', None, '2.13.1'),
        ('2.13.2', '2.13', '2.13.1'),
        ('2.13.2', '2.13.3', '2.13.4'),
    ])
    def test_call_invalid_version(self, swimlane_version, min_version, max_version):
        """Test that InvalidServerVersion is raised when calling a method with an out of range Swimlane version"""
        mock_swimlane = mock.MagicMock()
        mock_swimlane.build_version = swimlane_version

        resolver_class = self._get_resolver(min_version, max_version)

        resolver = resolver_class(mock_swimlane)

        with pytest.raises(InvalidSwimlaneBuildVersion):
            resolver.func()

    @pytest.mark.parametrize('swimlane_version,min_version,max_version', [
        ('2.13', '2.12', None),
        ('2.13', '2.13', None),
        ('2.13.2', '2.12', None),
        ('2.13', None, '2.13'),
        ('2.13.2', None, '2.13.3'),
        ('2.13.2', '2.13', '2.14'),
        ('2.13.2', '2.13.0', '2.14'),
        ('2.13.2', '2.13.0', '2.14.1'),
        ('2.13', '2.13', '2.14.1'),
    ])
    def test_call_valid_version(self, swimlane_version, min_version, max_version):
        """Test that InvalidServerVersion is raised when calling a method with an out of range Swimlane version"""
        mock_swimlane = mock.MagicMock()
        mock_swimlane.build_version = swimlane_version

        resolver_class = self._get_resolver(min_version, max_version)

        resolver = resolver_class(mock_swimlane)

        args = (1, 2, 3)
        kwargs = {'a': 'A', 'b': 'B'}

        assert resolver.func(*args, **kwargs) == (args, kwargs)
