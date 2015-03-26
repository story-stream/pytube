from unittest import TestCase
from apiclient.http import HttpMock
from pytube import PyTubeNotFound
from pytube.client import PyTubeClient


class ClientTestCase(TestCase):
    def setUp(self):
        self.api_key = 'AIzaSyDxIf48UpW3J77OHlssoME4rFXJ-ugSeZ8'

    def test_raises_exception_where_username_isnt_supplied_when_checking_for_valid_username(self):
        client = PyTubeClient(self.api_key)
        self.assertRaises(PyTubeNotFound, client.is_valid_username, None)

    def test_raises_exception_where_username_doesnt_exist_when_checking_for_valid_username(self):
        client = self.__build_client('channel_doesnt_exist.json')

        self.assertRaises(PyTubeNotFound, client.is_valid_username, 'rwerwer')

    def test_doesnt_raise_exception_where_username_exists_when_checking_for_valid_username(self):
        client = self.__build_client('channel_exists.json')

        self.assertTrue(client.is_valid_username('porsche'))

    def test_raises_exception_when_username_isnt_supplied_when_trying_to_retrieve_videos_for_username(self):
        client = PyTubeClient(self.api_key)
        self.assertRaises(PyTubeNotFound, client.get_videos_for, None)

    def test_raises_exception_where_username_doesnt_exist_when_trying_to_retrieve_videos_for_username(self):
        client = self.__build_client('channel_doesnt_exist.json')
        self.assertRaises(PyTubeNotFound, client.get_videos_for, 'rwerwer')

    def test_can_retrieve_videos_for_user_when_username_is_valid(self):
        client = self.__build_client('channel_exists.json')

        videos, video_meta = client.get_videos_for('porsche', mocks={
            'playlistItems': self.__build_mock('playlistitems.json')
        })

        self.assertEqual(10, len(videos))

    def test_can_retrieve_videos_with_additional_meta_data_for_user_when_username_is_valid(self):
        client = self.__build_client('channel_exists.json')

        videos, video_meta = client.get_videos_for('porsche', mocks={
            'playlistItems': self.__build_mock('playlistitems.json'),
            'videos': self.__build_mock('videos.json')
        })

        self.assertEqual(10, len(videos))
        video = videos[0]

        self.assertEqual(video['author_name'], 'Porsche')
        self.assertEqual(video['title'], 'OMG I LOVE CHEESE')
        self.assertEqual(video['rating']['average'], 'abc')
        self.assertEqual(video['statistics']['views'], 'abc')

    def test_can_retrieve_video(self):
        video = self.client.get_video('RFs1M47ZWA8')

        self.assertEqual(video['title'][:32], '10 year old guitarist Alex Ayres')

    def __build_client(self, mock_file):
        http = self.__build_mock(mock_file)
        return PyTubeClient(self.api_key, http_mock=http)

    def __build_mock(self, mock_file):
        import os

        path = os.path.dirname(__file__)
        fixture_path = os.path.join(path, 'fixtures', mock_file)

        return HttpMock(fixture_path, {'status': '200'})