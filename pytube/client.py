import http

from .parser import YoutubeParser
from pytube import PyTubeNotFound


class PyTubeClient(object):
    __urls = {
        'user_videos': 'http://gdata.youtube.com/feeds/api/users/{0}/uploads?v=2',
        'video': 'https://gdata.youtube.com/feeds/api/videos/{0}?v=2'
    }

    def __init__(self):
        self.__parser = YoutubeParser()

    def get_videos_for(self, username):
        res = http.get(self.__urls['user_videos'].format(username))

        if res[0] != '<':
            raise PyTubeNotFound(res)

        entries = self.__parser.get_entries(res)
        if not entries:
            raise PyTubeNotFound('User not found')

        return entries

    def get_video(self, video_id, html_description=True):
        res = http.get(self.__urls['video'].format(video_id))

        if res[0] != '<':
            raise PyTubeNotFound(res)

        entry = self.__parser.get_video(res)
        if not entry:
            raise PyTubeNotFound('Video not found')

        return entry

