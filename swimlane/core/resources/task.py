"""This module provides a Task class."""

from ..auth import Client
from .resource import Resource


class Task(Resource):
    """A simple abstraction of a Swimlane task."""

    def __init__(self, fields):
        """Init a Task with fields.

        Args:
            fields (dict): A dict of fields and values.
        """
        super(Task, self).__init__(fields)

    def run(self, record):
        """Run a task.

        Args:
            record (Record): The record to run this task against.
        """
        Client.post({
            "taskId": self.id,
            "record": record._fields
        }, "task/execute/record")

    @classmethod
    def find_all(cls):
        """Find all Tasks in the system.

        Returns:
            A generator that yields Tasks.
        """
        return (Task(t) for t in Client.get("task/light"))

    @classmethod
    def find(cls, name):
        """Find all Tasks in the system.

        Args:
            name (str): The task name.

        Returns:
            A Task.
        """
        return next((t for t in cls.find_all() if t.name == name), None)

