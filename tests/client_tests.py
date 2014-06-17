import unittest
from pytube.client import PyTubeClient, PyTubeNotFound


class ClientTestCase(unittest.TestCase):
    def test_raises_exception_for_erroneous_user(self):
        client = PyTubeClient()

        self.assertRaises(PyTubeNotFound, client.get_videos_for, 'rwerwer')

    def test_can_retrieve_videos(self):
        client = PyTubeClient()

        videos = client.get_videos_for('porsche')

        self.assertEqual(len(videos), 25)

    def test_can_retrieve_video(self):
        client = PyTubeClient()

        video = client.get_video('TqoUfpe0Ef8')

        print video

        self.assertEqual(video['title'][:32], 'Brighton Pride Welcomes you.')
        self.assertEqual(video['description'], None)