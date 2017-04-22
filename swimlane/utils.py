import random
import string


def random_string(length, source=string.ascii_letters + string.digits):
    """Return random string of characters from source of specified length"""
    return ''.join(random.choice(source) for _ in range(length))


def get_recursive_subclasses(cls):
    """Return list of all subclasses for a class, including subclasses of direct subclasses"""
    return cls.__subclasses__() + [g for s in cls.__subclasses__() for g in get_recursive_subclasses(s)]
