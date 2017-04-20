import random
import string


def random_string(length, source=string.ascii_letters + string.digits):
    return ''.join(random.choice(source) for _ in range(length))


def get_recursive_subclasses(cls):
    return cls.__subclasses__() + [g for s in cls.__subclasses__() for g in get_recursive_subclasses(s)]
