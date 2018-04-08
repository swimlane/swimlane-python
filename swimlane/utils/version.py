import functools
import re

from pkg_resources import get_distribution, DistributionNotFound

from swimlane.exceptions import InvalidSwimlaneBuildVersion


def compare_versions(version_a, version_b, zerofill=False):
    """Return direction of version relative to provided version sections

    Args:
        version_a (str): First version to compare
        version_b (str): Second version to compare
        zerofill (bool): If True, treat any missing version sections as 0, otherwise ignore section. Defaults to False

    Returns:
        int: 0 if equal, -1 if a > b, 1 if a < b

    Examples:

        If a is equal to b, return 0
        If a is greater than b, return -1
        If a is less than b, return 1

        >>> compare_versions('2', '2') == 0
        >>> compare_versions('2', '1') == -1
        >>> compare_versions('2', '3') == 1

        If zerofill is False (default), sections not included in both versions are ignored during comparison

        >>> compare_versions('2.13.2', '2.13') == 0
        >>> compare_versions('2.13.2-1234', '3') == 1

        If zerofill is True, any sections in one version not included in other version are set to 0

        >>> compare_versions('2.13.2', '2.13', True) == -1
        >>> compare_versions('2.13.2-1234', '2.13.2', True) == -1
        >>> compare_versions('2.13.2', '2.13.2', True) == 0
    """
    a_sections = list((int(match) for match in re.findall(r'\d+', version_a)))
    b_sections = list((int(match) for match in re.findall(r'\d+', version_b)))

    if zerofill:
        max_sections = max([len(a_sections), len(b_sections)])

        a_sections += [0 for _ in range(max(max_sections - len(a_sections), 0))]
        b_sections += [0 for _ in range(max(max_sections - len(b_sections), 0))]

    else:
        min_sections = min([len(a_sections), len(b_sections)])

        a_sections = a_sections[:min_sections]
        b_sections = b_sections[:min_sections]

    return (b_sections > a_sections) - (b_sections < a_sections)


def requires_swimlane_version(min_version=None, max_version=None):
    """Decorator for SwimlaneResolver methods verifying Swimlane server build version is within a given inclusive range

    Raises:
        InvalidVersion: Raised before decorated method call if Swimlane server version is out of provided range
        ValueError: If neither min_version or max_version were provided, or if those values conflict (2.15 < 2.14)
    """

    if min_version is None and max_version is None:
        raise ValueError('Must provide either min_version, max_version, or both')

    if min_version and max_version and compare_versions(min_version, max_version) < 0:
        raise ValueError('min_version must be <= max_version ({}, {})'.format(min_version, max_version))

    def decorator(func):

        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            swimlane = self._swimlane

            if min_version and compare_versions(min_version, swimlane.build_version, True) < 0:
                raise InvalidSwimlaneBuildVersion(swimlane, min_version, max_version)

            if max_version and compare_versions(swimlane.build_version, max_version, True) < 0:
                raise InvalidSwimlaneBuildVersion(swimlane, min_version, max_version)

            return func(self, *args, **kwargs)

        return wrapper

    return decorator


def get_package_version():
    """Get swimlane package version

    Returns:
         str: Installed swimlane lib package version, or 0.0.0.dev if not fully installed
    """
    try:
        return get_distribution(__name__.split('.')[0]).version
    except DistributionNotFound:
        return '0.0.0.dev'
