import os
import string
import sys

import mock
import pytest
from pkg_resources import DistributionNotFound

from swimlane.utils import (
    random_string,
    get_recursive_subclasses,
    import_submodules,
    compare_versions,
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
    ((2,), 0),
    ((1,), 1),
    ((3,), -1),
    ((2, 13), 0),
    ((2, 12), 1),
    ((2, 14), -1),
    ((2, 13, 3), -1),
    ((2, 13, 2), 0),
    ((2, 13, 2, 173414), 0),
    ((2, 13, 2, 173415), -1)
])
def test_compare_versions(inputs, expected):
    """Test compare versions"""
    mock_swimlane = mock.MagicMock()
    mock_swimlane.version = '2.13.2-173414'

    assert compare_versions(mock_swimlane, *inputs) == expected


def test_get_package_version():
    mock_dist = mock.MagicMock()
    mock_dist.version = '1.2.3'

    with mock.patch('swimlane.utils.get_distribution', return_value=mock_dist):
        version = get_package_version()
        assert tuple(version.split('.')[:2]) > ('0', '0', '0')

    with mock.patch('swimlane.utils.get_distribution', side_effect=DistributionNotFound):
        assert get_package_version() == '0.0.0.dev'
