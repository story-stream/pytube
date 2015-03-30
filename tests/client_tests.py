#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from unittest import TestCase
from apiclient.http import HttpMock
from pytube import PyTubeNotFoundException, PyTubeException
from pytube.client import PyTubeClient


class ClientTestCase(TestCase):
    def setUp(self):
        self.api_key = 'AIzaSyDxIf48UpW3J77OHlssoME4rFXJ-ugSeZ8'

    def test_returns_true_when_username_is_a_channel_id(self):
        client = PyTubeClient(self.api_key)
        self.assertTrue(client.is_channel_id('UCsyZmMdOxKubW1mrJBAoE-Q'))

    def test_returns_false_when_username_is_not_a_channel_id(self):
        client = PyTubeClient(self.api_key)
        self.assertFalse(client.is_channel_id('porsche'))

    def test_raises_exception_when_checking_for_channel_id_and_value_is_none(self):
        client = PyTubeClient(self.api_key)
        self.assertRaises(PyTubeException, client.is_channel_id, None)

    def test_raises_exception_when_checking_for_channel_id_and_value_is_empty_string(self):
        client = PyTubeClient(self.api_key)
        self.assertRaises(PyTubeException, client.is_channel_id, '')

    def test_raises_exception_where_username_isnt_supplied_when_checking_for_valid_username(self):
        client = PyTubeClient(self.api_key)
        self.assertRaises(PyTubeNotFoundException, client.is_valid_identifier, None)

    def test_raises_exception_where_username_doesnt_exist_when_checking_for_valid_username(self):
        client = self.__build_client('channel_doesnt_exist.json')

        self.assertRaises(PyTubeNotFoundException, client.is_valid_identifier, 'rwerwer')

    def test_doesnt_raise_exception_where_username_exists_when_checking_for_valid_username(self):
        client = self.__build_client('channel_exists.json')

        self.assertTrue(client.is_valid_identifier('porsche'))

    def test_raises_exception_when_username_isnt_supplied_when_trying_to_retrieve_videos_for_username(self):
        client = PyTubeClient(self.api_key)
        self.assertRaises(PyTubeNotFoundException, client.get_videos_for, None)

    def test_raises_exception_where_username_doesnt_exist_when_trying_to_retrieve_videos_for_username(self):
        client = self.__build_client('channel_doesnt_exist.json')
        self.assertRaises(PyTubeNotFoundException, client.get_videos_for, 'rwerwer')

    def test_can_retrieve_videos_for_user_when_username_is_valid(self):
        client = self.__build_client('channel_exists.json')

        videos = client.get_videos_for('porsche', mocks={
            'playlistItems': self.__build_mock('playlistitems.json')
        })

        self.assertEqual(10, len(videos))

    def test_can_retrieve_videos_with_additional_meta_data_for_user_when_username_is_valid(self):
        client = self.__build_client('channel_exists.json')

        videos = client.get_videos_for('porsche', mocks={
            'playlistItems': self.__build_mock('playlistitems.json'),
            'videos': self.__build_mock('videos.json')
        })

        self.assertEqual(10, len(videos))
        video = videos[0]

        self.assertEqual(video['author_name'], 'Porsche')
        self.assertEqual(video['title'], u'Behind the wheel of the Cayman GT4 with Walter Röhrl')
        self.assertEqual(int(video['rating']['likes']), 329)
        self.assertEqual(int(video['statistics']['views']), 59940)

    def test_can_retrieve_video(self):
        client = self.__build_client('single_video.json')

        video = client.get_video('RFs1M47ZWA8')

        self.assertEqual(video['title'], 'Protone Pedals Attack Overdrive')
        self.assertEqual(int(video['rating']['likes']), 573)
        self.assertEqual(int(video['statistics']['views']), 29856)

    def test_raises_exception_when_video_id_not_found(self):
        client = self.__build_client('single_video.json', status=404)

        self.assertRaises(PyTubeNotFoundException, client.get_video, 'RFs1M47ZWA8')

    def __build_client(self, mock_file, status=200):
        http = self.__build_mock(mock_file, status)
        return PyTubeClient(self.api_key, http_mock=http)

    def __build_mock(self, mock_file, status=200):
        import os

        path = os.path.dirname(__file__)
        fixture_path = os.path.join(path, 'fixtures', mock_file)

        return HttpMock(fixture_path, {'status': status})