from swimlane.core.resolver import SwimlaneResolver
from swimlane.core.cache import check_cache
from swimlane.core.resources.task import Task
from swimlane.utils import one_of_keyword_only
from typing import Optional, List, Any



class TaskAdapter(SwimlaneResolver):
    """Handles retreival of Swimlane Task Resources and execution of tasks against records."""

    @check_cache(Task)
    @one_of_keyword_only('id', 'name')
    def get(self, key: str, value: str) -> Optional[Task]:
        """Get a single task by id or name"""
        if key == 'id':
            response = self._swimlane.request('get', 'task/{id}'.format(id=value))
            return Task(self._swimlane, response.json())

        if key == 'name':
            response = self._swimlane.request('get', 'task/light')
            for task in response.json():
                if value == task.get('name'):
                    return self._get_full(task.get('id'))
            raise ValueError('No task with name "{value}"'.format(value=value))

    def list(self) -> List[Task]:
        """Retrieve list of all tasks.

        Returns:
            :class:`list` of :class:`~swimlane.core.resources.task.Task`: List of all tasks.
        """
        response = self._swimlane.request('get', 'task/light')
        return [self._get_full(item.get('id')) for item in response.json()]

    def execute(self, task_name: str, raw_record) -> Any:
        """Execute job by name.

        Returns:
            Response of request from the API endpoint.
        """
        task_id = self.get(name=task_name).id
        data = {
            'taskId': task_id,
            'record': raw_record,
        }
        return self._swimlane.request('post', 'task/execute/record', json=data)

    def _get_full(self, task_id: str) -> Task:
        """Retreived complete task raw json of task from API.

        Returns:
            :class:`~swimlane.core.resources.task.Task`: Single Task object.
        """
        response = self._swimlane.request('get', 'task/{task_id}'.format(task_id=task_id))
        return Task(self._swimlane, response.json())
