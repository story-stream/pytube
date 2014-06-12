import requests
from pytube import PyTubeNotFound


def get(url):
    try:
        res = requests.get(url)
        if res.status_code is not 404:
            return res.content
        else:
            raise PyTubeNotFound('Unable to find feed')

    except requests.ConnectionError:
        raise PyTubeNotFound('Unable to connect to url. Is your internet connection up?')