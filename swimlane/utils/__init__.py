"""Utility functions"""
from __future__ import absolute_import

import importlib
import pkgutil
import random
import string
import functools


def random_string(length, source=string.ascii_letters + string.digits):
    """Return random string of characters from source of specified length

    Args:
        length (int): Length of the returned string
        source (str): String of characters to use as options for randomly selected characters. Defaults to alphanumeric

    Returns:
        str: String of length number of characters composed of source characters
    """
    return ''.join(random.choice(source) for _ in range(length))


def get_recursive_subclasses(cls):
    """Return list of all subclasses for a class, including subclasses of direct subclasses"""
    return cls.__subclasses__() + [g for s in cls.__subclasses__() for g in get_recursive_subclasses(s)]


def import_submodules(package):
    """Return list of imported module instances from beneath root_package"""

    if isinstance(package, str):
        package = importlib.import_module(package)

    results = {}

    for _, full_name, is_pkg in pkgutil.walk_packages(package.__path__, package.__name__ + '.'):
        results[full_name] = importlib.import_module(full_name)

        if is_pkg:
            results.update(import_submodules(full_name))

    return results


def one_of_keyword_only(*valid_keywords):
    """Decorator to help make one-and-only-one keyword-only argument functions more reusable

    Notes:
        Decorated function should take 2 arguments, the first for the key, the second the value

    Examples:

        ::

            @one_of_keyword_only('a', 'b', 'c')
            def func(key, value):
                if key == 'a':
                    ...
                elif key == 'b':
                    ...
                else:
                    # key = 'c'
                    ...

            ...

            func(a=1)
            func(b=2)
            func(c=3)

            try:
                func(d=4)
            except TypeError:
                ...

            try:
                func(a=1, b=2)
            except TypeError:
                ...

    Args:
        *valid_keywords (str): All allowed keyword argument names

    Raises:
        TypeError: On decorated call, if 0 or 2+ arguments are provided or kwargs contains a key not in valid_keywords
    """

    def decorator(func):

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            sentinel = object()
            values = {}

            for key in valid_keywords:
                kwarg_value = kwargs.pop(key, sentinel)
                if kwarg_value is not sentinel:
                    values[key] = kwarg_value

            if kwargs:
                raise TypeError('Unexpected arguments: {}'.format(kwargs))

            if not values:
                raise TypeError('Must provide one of {} as keyword argument'.format(', '.join(valid_keywords)))

            if len(values) > 1:
                raise TypeError('Must provide only one of {} as keyword argument. Received {}'.format(
                    ', '.join(valid_keywords),
                    values
                ))

            return func(*(args + values.popitem()))

        return wrapper

    return decorator

