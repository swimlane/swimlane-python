import binascii
import copy
import os
import time

from .core.resources import App


def random_objectid():
    """Returns a randomly generated MongoDB ObjectId."""
    timestamp = '{0:x}'.format(int(time.time()))
    rest = binascii.b2a_hex(os.urandom(8)).decode('ascii')
    return timestamp + rest


def scrub(obj, *keys):
    """
    Recursively remove one or more keys from a dict or list object.

    :param obj: A dict or list to scrub.
    :type obj: dict or list
    :param keys: One or more keys to remove.
    :param keys: str
    """
    if isinstance(obj, dict):
        for k in obj.keys():
            if k in keys:
                del obj[k]
            else:
                scrub(obj[k], *keys)
    elif isinstance(obj, list):
        for i in reversed(range(len(obj))):
            if obj[i] in keys:
                del obj[i]
            else:
                scrub(obj[i], *keys)
    else:
        pass


def get_by_key_value(obj, key, value, default=None):
    """
    Returns an object in a list with a matching key and value.

    :param obj: The list to search for object.
    :type obj: list
    :param key: The key to look for.
    :type key: str
    :param value: The value to look for.
    :type value: str
    :param default: Value to return if not found.
    :type default: any
    :returns: The object if it exists, otherwise the default value.
    :rtype: dict
    """
    return next((o for o in obj if key in o and o[key] == value), default)


def copy_field_values(src_app, src_field_name, dest_app, dest_field_name):
    """
    Copy a field's values from one field to another, only copying values
    that don't exist in the destination field. A best effort to preserve value
    order is made between the source and destination.

    :param src_app: The source app to copy from.
    :type src_app: :class:`App`
    :param src_field_name: the name of the field to copy from.
    :type src_field_name: str
    :param dest_app: The app to copy to.
    :type dest_app: :class:`App`
    :param dest_field_name: The name of the field to copy to.
    :type dest_field_name: str
    :returns: A tuple of added and moved values.
    :rtype: tuple
    """
    if not isinstance(src_app, App):
        raise TypeError('The src_app must be an instance of App')
    if not isinstance(dest_app, App):
        raise TypeError('The dest_app must be an instance of App')
    src_field = get_by_key_value(src_app.fields, 'name', src_field_name)
    if not src_field:
        raise ValueError('Field %s does not exist in source app' %
                         src_field_name)
    dest_field = get_by_key_value(dest_app.fields, 'name', dest_field_name)
    if not dest_field:
        raise ValueError('Field %s does not exist in destination app' %
                         dest_field_name)
    if src_field['fieldType'] != 'valuesList' or \
            dest_field['fieldType'] != 'valuesList':
        raise TypeError('Source and destination fields must be valuesList')
    added_values = []
    moved_values= []
    for src_index, src_value in enumerate(src_field['values']):
        dest_value = get_by_key_value(dest_field['values'], 'name',
                                      src_value['name'])
        if not dest_value:
            dest_value = src_value.copy()
            dest_value['id'] = random_objectid()
            dest_field['values'].insert(src_index, dest_value)
            added_values.append(dest_value)
        else:
            dest_index = dest_field['values'].index(dest_value)
            if src_index != dest_index:
                dest_value = dest_field['values'].pop(dest_index)
                dest_field['values'].insert(src_index, dest_value)
                moved_values.append(dest_value)
    if added_values or moved_values:
        dest_app.save()
    return added_values, moved_values
