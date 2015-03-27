from apiclient.discovery import build
from googleapiclient.errors import HttpError
from pytube import PyTubeNotFound
from pytube.parser import PyTubeParser

YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"


class PyTubeClient(object):
    def __init__(self, api_key, http_mock=None):
        self.youtube_client = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=api_key)
        self.http_mock = http_mock
        self.parser = PyTubeParser()

    def is_valid_username(self, username):
        """
        Checks to see whether the username supplied is a valid Youtube username.
        Returns true if it is, raises PyTubeNotFound if not.
        """
        if not username:
            raise PyTubeNotFound(u'You must specify a username')

        channels = self._get_channels_for_username(username)

        if channels:
            return True
        else:
            raise PyTubeNotFound(u'User {} not found'.format(username))

    def get_video(self, video_id):
        """
        Retrieves a single video record
        :param video_id: youtube id of the video to retrieve
        """
        try:
            video_response = self.youtube_client.videos().list(
                part='snippet,statistics,recordingDetails',
                id=video_id
            ).execute(http=self.http_mock)
        except HttpError:
            raise PyTubeNotFound('Video cannot be found')

        videos = video_response.get('items', [])
        if videos:
            video_record = videos[0]

            video = self.parser.parse_single_video(video_record)
            video.update(self.parser.parse_video_meta(video_record))

            return video

        raise PyTubeNotFound('Video cannot be found')

    def get_videos_for(self, username, **kwargs):
        """
        Retrieves a list of videos belonging to the specified username, which is constructed via a number of
        Youtube Data API calls.
        If username is not valid, it raises PyTubeNotFound
        """

        mock_requests = kwargs.get('mocks', {})

        if not username:
            raise PyTubeNotFound(u'You must specify a username')

        channels = self._get_channels_for_username(username)

        if channels:
            playlist_id = channels[0].get('contentDetails', {}).get('relatedPlaylists', {}).get('uploads')
            if not playlist_id:
                raise PyTubeNotFound(u'Could not find the "uploads" playlist for {}'.format(username))

            playlist_items = self._get_playlist_items_for_playlist(playlist_id,
                                                                   http_mock=mock_requests.get('playlistItems'))

            if playlist_items:
                video_meta = self._get_video_meta_for_videos(playlist_items, http_mock=mock_requests.get('videos'))
                return self.parser.parse_videos(username, playlist_items, video_meta)
            return None

        else:
            raise PyTubeNotFound(u'User {} not found'.format(username))

    def _get_channels_for_username(self, username):
        """
        Retrieves the channel information for a given username. It will return some basic user information
        such as title and description (amongst others), but also returns the playlist ids belonging to that user
        """
        try:
            channels_response = self.youtube_client.channels().list(
                forUsername=username,
                part='contentDetails'
            ).execute(http=self.http_mock)
        except HttpError:
            raise PyTubeNotFound(u'Channel for {} cannot be found'.format(username))

        return channels_response.get('items', [])

    def _get_playlist_items_for_playlist(self, playlist_id, results_per_page=50, page_token=None, http_mock=None):
        """
        Retrives a list of videos which belong to a playlist. The data returned in this response includes video title,
        description, thumbnails and video id
        :param playlist_id: id of the playlist to retrieve videos for
        :param results_per_page: number of results to return per request
        :param page_token: the token to retrieve subsequant pages of data
        :param http_mock: HttpMock object used within unittesting to mock the API response
        :return: list of dict items relating to videos belonging to the playlist
        """
        try:
            playlist_response = self.youtube_client.playlistItems().list(
                part='snippet',
                playlistId=playlist_id,
                maxResults=results_per_page,
                pageToken=page_token
            ).execute(http=http_mock)
        except HttpError:
            raise PyTubeNotFound('Playlist with id {} cannot be found'.format(playlist_id))

        playlist_items = playlist_response.get('items', [])
        videos = []

        if playlist_items:
            for item in playlist_items:
                item_snippet = item.get('snippet')
                if item_snippet:
                    videos.append(item_snippet)

        return videos

    def _get_video_meta_for_videos(self, playlist_items, http_mock=None):
        """
        Retrieves a list of meta data against a collections of playlistItems
        :param playlist_items: list of playlistItems
        :param http_mock: HttpMock object used within unittesting to mock the API response
        :return: list of dict items relating to video meta data belonging to the playlist items
        """
        try:
            video_response = self.youtube_client.videos().list(
                part='statistics,recordingDetails',
                id=map(lambda v: v['resourceId']['videoId'], playlist_items),
                maxResults=len(playlist_items)
            ).execute(http=http_mock)
        except HttpError:
            raise PyTubeNotFound('Videos cannot be found {}'.format(playlist_items))

        data = {}

        for video in video_response.get('items', []):
            data[video['id']] = video

        return data
