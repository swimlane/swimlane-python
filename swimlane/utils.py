"""Utility functions"""

import importlib
import pkgutil
import random
import string
import re
from pkg_resources import DistributionNotFound, get_distribution


def random_string(length, source=string.ascii_letters + string.digits):
    """Return random string of characters from source of specified length"""
    return ''.join(random.choice(source) for _ in range(length))


def get_recursive_subclasses(cls):
    """Return list of all subclasses for a class, including subclasses of direct subclasses"""
    return cls.__subclasses__() + [g for s in cls.__subclasses__() for g in get_recursive_subclasses(s)]


def import_submodules(package):
    """Return list of imported module instances from beneath root_package"""

    if isinstance(package, str):
        package = importlib.import_module(package)

    results = {}

    for _, name, is_pkg in pkgutil.walk_packages(package.__path__):
        full_name = package.__name__ + '.' + name
        results[full_name] = importlib.import_module(full_name)

        if is_pkg:
            results.update(import_submodules(full_name))

    return results


def compare_versions(swimlane, *version_sections):
    """Return direction of Swimlane version relative to provided version sections
    
    If Swimlane version is equal to provided version, return 0
    If Swimlane version is greater than provided version, return 1
    If Swimlane version is less than provided version, return -1
    
    e.g. with Swimlane version = 2.13.2-173414
        _compare_version(2) = 0
        _compare_version(1) = 1
        _compare_version(3) = -1
        
        _compare_version(2, 13) = 0
        _compare_version(2, 12) = 1
        _compare_version(2, 14) = -1
        
        _compare_version(2, 13, 3) = -1
        
        _compare_version(2, 13, 2, 173415) = -1
    """
    sections_provided = len(version_sections)

    versions = tuple([int(match) for match in re.findall(r'\d+', swimlane.version)[0:sections_provided]])

    return (versions > version_sections) - (versions < version_sections)


def get_package_version():
    """Return swimlane lib package version, or 0.0.0-dev if not available"""
    try:
        return get_distribution(__name__.split('.')[0]).version
    except DistributionNotFound:
        return '0.0.0-dev'
