"""Utility functions"""
from __future__ import absolute_import

import importlib
import pkgutil
import random
import string


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
