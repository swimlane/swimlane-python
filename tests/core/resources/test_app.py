import mock
import unittest

from swimlane.core.resources import App


MOCK_APP = {
    'id': '123',
    'name': 'Mock App',
    'acronym': 'MA',
    'fields': [{
        'id': '456',
        'name': 'Mock Field'
    }]
}


class AppTestCase(unittest.TestCase):
    def test_init(self):
        app = App(MOCK_APP)
        for key, value in MOCK_APP.items():
            self.assertEqual(getattr(app, key), value)

    def test_field_id(self):
        app = App(MOCK_APP)
        self.assertEqual(app.field_id('Mock Field'), '456')
        self.assertEqual(app.field_id('Not A Field'), None)

    @mock.patch('swimlane.core.resources.app.Client', autospec=True)
    def test_find_all(self, mock_client):
        mock_client.get.return_value = [MOCK_APP]
        apps = list(App.find_all())
        self.assertEqual(len(apps), 1)
        self.assertIsInstance(apps[0], App)

    @mock.patch('swimlane.core.resources.app.Client', autospec=True)
    def test_find_by_id(self, mock_client):
        mock_client.get.return_value = MOCK_APP
        app = App.find(app_id='123')
        self.assertIsInstance(app, App)
        self.assertEqual(app.id, '123')

    @mock.patch('swimlane.core.resources.app.Client', autospec=True)
    def test_find_by_name(self, mock_client):
        mock_client.get.return_value = [MOCK_APP]
        app = App.find(name='Mock App')
        self.assertIsInstance(app, App)
        self.assertEqual(app.name, 'Mock App')

    @mock.patch('swimlane.core.resources.app.Client', autospec=True)
    def test_find_by_acronym(self, mock_client):
        mock_client.get.return_value = [MOCK_APP]
        app = App.find(acronym='MA')
        self.assertIsInstance(app, App)
        self.assertEqual(app.acronym, 'MA')

    @mock.patch('swimlane.core.resources.app.Client', autospec=True)
    def test_find_by_name_does_not_exist(self, mock_client):
        mock_client.get.return_value = [MOCK_APP]
        app = App.find(name='Some Other App')
        self.assertIsNone(app)

    @mock.patch('swimlane.core.resources.app.Client', autospec=True)
    def test_find_by_acronym_does_not_exist(self, mock_client):
        mock_client.get.return_value = [MOCK_APP]
        app = App.find(acronym='SOA')
        self.assertIsNone(app)
