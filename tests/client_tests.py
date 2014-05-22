import unittest
from pytube.client import PyTubeClient, PyTubeNotFound


class ClientTestCase(unittest.TestCase):
    def test_raises_exception_for_erroneous_user(self):
        client = PyTubeClient()

        self.assertRaises(PyTubeNotFound, client.get_videos, 'rwerwer')

    def test_can_retrieve_videos(self):
        client = PyTubeClient()

        videos = client.get_videos('porsche')

        self.assertEqual(len(videos), 25)