import json
import pytest
import mock
from requests.models import Response
from swimlane.core.adapters import TaskAdapter
from swimlane.core.resources.task import Task


@pytest.fixture(name='mock_task_adapter')
def fixture_mock_task_adapter(mock_swimlane):
    yield TaskAdapter(mock_swimlane)


@pytest.mark.parametrize('mock_task', [
    ('sample_task.json')
    ], indirect=['mock_task'])
def test_get(mock_task, mock_task_adapter, test_data):
    mock_task_response = mock.Mock(spec=Response)
    with mock.patch.object(mock_task_adapter._swimlane, 'request', return_value=mock_task_response):
        mock_task_response.status_code = 200
        mock_task_response.json.return_value = mock_task._raw
        # Test by id
        task = mock_task_adapter.get(id=mock_task.id)
        assert task.id == mock_task.id


    mock_task_response.reset_mock()
    with mock.patch.object(mock_task_adapter._swimlane, 'request', return_value=mock_task_response):
        # Test by Name
        mock_task_response.status_code = 200
        mock_task_response.json.return_value = json.load((test_data / 'task_light.json').open())
        with mock.patch.object(mock_task_adapter, '_get_full', return_value=mock_task):
            task = mock_task_adapter.get(name=mock_task.name)
            assert task.name == mock_task.name


            # Test name not found raises ValueError
            name_does_not_exist = 'name_does_not_exist'
            with pytest.raises(ValueError) as exec_info:
                mock_task_adapter.get(name=name_does_not_exist)
            
            assert str(exec_info.value) == str(ValueError('No task with name "{}"'.format(name_does_not_exist)))

            invalid_key = 'invalid_key'
            invalid_key_value = 'Invalid'
            with pytest.raises(TypeError) as exec_info:
                mock_task_adapter.get(invalid_key=invalid_key_value)
            
            assert str(exec_info.value) == str(TypeError('Unexpected arguments: {}'.format(
                {invalid_key: invalid_key_value})))


@pytest.mark.parametrize('mock_task', [
     ('sample_task.json')
     ], indirect=['mock_task'] )       
def test_list(mock_task, mock_task_adapter):
    mock_task_response = mock.Mock(spec=Response)
    with mock.patch.object(mock_task_adapter._swimlane, 'request', return_value=mock_task_response):
        mock_task_response.status_code = 200
        mock_task_response.json.return_value = [mock_task._raw]
        with mock.patch.object(mock_task_adapter, '_get_full', return_value=mock_task):
            task_list = mock_task_adapter.list()
            assert isinstance(task_list, list)
            for task in task_list:
                assert isinstance(task, Task)


@pytest.mark.parametrize('mock_task', [
     ('sample_task.json')
     ], indirect=['mock_task'] )   
def test_execute(mock_task_adapter, mock_task, mock_record):
    with mock.patch.object(mock_task_adapter, 'get', return_value=mock_task):
        mock_response = mock.Mock(spec=Response)
        with mock.patch.object(mock_task_adapter._swimlane, 'request', return_value=mock_response) as mock_request:
            response = mock_task_adapter.execute(mock_task.name, mock_record._raw)
            assert response == mock_response
            expected_json = {
                'taskId': mock_task.id,
                'record': mock_record._raw,
            }
            mock_request.assert_has_calls(calls=[mock.call('post', 'task/execute/record', json=expected_json)])
            assert mock_request.call_count == 1


@pytest.mark.parametrize('mock_task', [
     ('sample_task.json')
     ], indirect=['mock_task'] ) 
def test_get_full(mock_task, mock_task_adapter):
    mock_response = mock.Mock(spec=Response)
    with mock.patch.object(mock_task_adapter._swimlane, 'request', return_value=mock_response):
        mock_response.json.return_value = mock_task._raw
        task_object = mock_task_adapter._get_full(mock_task.id)
        assert isinstance(task_object, Task)
        assert task_object.id == mock_task.id
        assert task_object.name == mock_task.name
        assert task_object.app_id == mock_task.app_id
        assert task_object.script == mock_task.script
 