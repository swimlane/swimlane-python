from mock import patch
import unittest

from swimlane.core.resources import App


class AppTestCase(unittest.TestCase):
    def test_init(self):
        a = App({'id': '123', 'name': 'Incident Response', 'acronym': 'IR'})

        self.assertEqual(a.id, '123')
        self.assertEqual(a.name, 'Incident Response')
        self.assertEqual(a.acronym, 'IR')

    def test_field_id(self):
        a = App({'fields': [{'id': '123', 'name': 'foo'}]})

        self.assertEqual(a.field_id('foo'), '123')
        self.assertEqual(a.field_id('bar'), None)

    @patch('swimlane.core.resources.app.Client', autospec=True)
    def test_find_all(self, mock_client):
        mock_client.get.return_value = [
            {'id': '123', 'name': 'Some Application'}]
        a = list(App.find_all())

        self.assertEqual(len(a), 1)
        self.assertIsInstance(a[0], App)

    @patch('swimlane.core.resources.app.Client', autospec=True)
    def test_find_by_id(self, mock_client):
        mock_client.get.return_value = \
            {'id': '123', 'name': 'Some App', 'acronym': 'SA'}
        a = App.find(app_id='123')
        self.assertIsInstance(a, App)
        self.assertEqual(a.id, '123')

    @patch('swimlane.core.resources.app.Client', autospec=True)
    def test_find_by_name(self, mock_client):
        mock_client.get.return_value = [
            {'id': '123', 'name': 'Some App', 'acronym': 'SA'}]
        a = App.find(name='Some App')
        self.assertIsInstance(a, App)
        self.assertEqual(a.name, 'Some App')

    @patch('swimlane.core.resources.app.Client', autospec=True)
    def test_find_by_acronym(self, mock_client):
        mock_client.get.return_value = [
            {'id': '123', 'name': 'Some App', 'acronym': 'SA'}]
        a = App.find(acronym='SA')
        self.assertIsInstance(a, App)
        self.assertEqual(a.acronym, 'SA')

    @patch('swimlane.core.resources.app.Client', autospec=True)
    def test_find_by_name_does_not_exist(self, mock_client):
        mock_client.get.return_value = [
            {'id': '123', 'name': 'Some App', 'acronym': 'SA'}]
        a = App.find(name='Some Other App')
        self.assertIsNone(a)

    @patch('swimlane.core.resources.app.Client', autospec=True)
    def test_find_by_acronym_does_not_exist(self, mock_client):
        mock_client.get.return_value = [
            {'id': '123', 'name': 'Some App', 'acronym': 'SA'}]
        a = App.find(acronym='SOA')
        self.assertIsNone(a)
