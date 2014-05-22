import requests

from .parser import YoutubeParser


class PyTubeClient(object):
    __urls = {
        'user_videos': 'http://gdata.youtube.com/feeds/api/users/{0}/uploads?orderby={1}'
    }

    def __init__(self):
        self.__parser = YoutubeParser()

    def get_videos(self, username, order_by='published'):
        res = self.__make_url_request(self.__urls['user_videos'].format(username, order_by))

        if res[0] != '<':
            raise PyTubeNotFound(res)

        entries = self.__parser.get_entries(res)
        if not entries:
            raise PyTubeNotFound('User not found')

        return entries

    def __make_url_request(self, url):
        try:
            res = requests.get(url)
            if res.status_code is not 404:
                return res.content
            else:
                raise PyTubeNotFound('Unable to find feed')

        except requests.ConnectionError:
            raise PyTubeNotFound('Unable to connect to url. Is your internet connection up?')


class PyTubeNotFound(BaseException):
    pass