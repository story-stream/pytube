import unittest
from pytube.client import PyTubeClient, PyTubeNotFound


class ClientTestCase(unittest.TestCase):
    def test_raises_exception_for_erroneous_user(self):
        client = PyTubeClient()

        self.assertRaises(PyTubeNotFound, client.get_videos, 'rwerwer')