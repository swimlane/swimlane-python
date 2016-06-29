"""This module provides a simple resource class."""


class Resource(object):
    """A simple abstraction over a Swimlane resource."""

    def __init__(self, fields):
        """Init a Resource with fields."""
        self._fields = fields

    def __getattr__(self, name):
        """Allow the internal fields dict to be retrievable as an attr.

        Args:
            name (str): The attr name.

        Returns:
            The value of self.fields[name] or AttributeError if name is
            not in self.fields.
        """
        if name in self._fields:
            return self._fields[name]

        raise AttributeError(name)

    def __setattr__(self, name, value):
        """Allow the internal fields dict to be settable as an attr.

        Args:
            name (str): The attr name.
            value: The value to set.
        """
        if "_fields" in self.__dict__ and name in self.__dict__["_fields"]:
            self.__dict__["_fields"][name] = value
            return

        self.__dict__[name] = value

    def __str__(self):
        """A string version."""
        return str(self._fields)

    @property
    def summary(self):
        return {k: v for k, v in self._fields.items()
                if k in ['id', 'name']}
