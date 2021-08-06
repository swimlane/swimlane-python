import json
from pathlib import Path
from shutil import copy as cp
import pytest
from swimlane.core.resources.app import App
from swimlane.core.resources.task import Task


@pytest.fixture(name='test_data', autouse=True, scope='module')
def fixture_test_data(tmp_path_factory):
    """
    Copies all files from fixtures/apps and fixtures/tasks folders to tmp_dir.
    """
    temp_path = tmp_path_factory.mktemp('data', numbered=False)
    app_files = Path(__file__).parent.joinpath('../fixtures/apps').glob('*')
    tasks_files = Path(__file__).parent.joinpath('../fixtures/tasks').glob('*')
    for file_name in app_files:
        cp(str(file_name), str(temp_path))
    for file_name in tasks_files:
        cp(str(file_name), str(temp_path))
    return temp_path


@pytest.fixture(name='mock_task_app')
def fixture_mock_task_app(test_data, mock_swimlane, request):
    full_path = (test_data / request.param)
    yield App(mock_swimlane, json.load(full_path.open()))


@pytest.fixture(name='mock_task')
def fixture_mock_task(test_data, mock_task_app, request):
    full_path = (test_data / request.param)
    yield Task(mock_task_app, json.load(full_path.open()))


@pytest.mark.parametrize('mock_task_app, mock_task, task_filename', [
    ('basic_app.json', 'sample_task.json', 'sample_task.json')
    ], indirect=['mock_task_app', 'mock_task'] )
def test_task_init(mock_task, mock_task_app, test_data, task_filename):
    task_json = json.load(test_data.joinpath(task_filename).open())
    task_name = task_json.get('name')
    assert mock_task.id == task_json.get('id')
    assert mock_task.name == task_name
    assert mock_task.app == mock_task_app
    assert mock_task.script == task_json.get('action').get('script')
    assert str(mock_task) == task_name
    assert mock_task.__repr__() == '<Task: {task_name}>'.format(task_name=task_name)

def test_task_not_associated_with_an_app():
    pytest.xfail('Write test.')
