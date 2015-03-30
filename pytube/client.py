from apiclient.discovery import build
from googleapiclient.errors import HttpError
from pytube import PyTubeNotFoundException, PyTubeException
from pytube.parser import PyTubeParser
import re

YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
YOUTUBE_CHANNEL_ID_PATTERN = r'^UC.{22}$'


class PyTubeClient(object):

    def __init__(self, api_key, http_mock=None):
        self.youtube_client = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=api_key)
        self.http_mock = http_mock
        self.parser = PyTubeParser()

    def is_channel_id(self, identifier):
        """
        Checks whether the supplied identifier conforms to the pattern of a Youtube channelId
        :param identifier: username or channel id
        :return: True if identifier matches pattern, False if not
        """

        if not identifier:
            raise PyTubeException(u'Identifier must be specified')

        return re.match(YOUTUBE_CHANNEL_ID_PATTERN, identifier) is not None

    def is_valid_identifier(self, identifier):
        """
        Checks to see whether the identifier supplied is a valid Youtube username.
        Returns true if it is, raises PyTubeNotFound if not.
        """
        if not identifier:
            raise PyTubeNotFoundException(u'You must specify an identifier')

        channels = self._get_channels_for(identifier)

        if channels:
            return True
        else:
            raise PyTubeNotFoundException(u'User/Channel {} not found'.format(identifier))

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
            raise PyTubeNotFoundException('Video cannot be found')

        videos = video_response.get('items', [])
        if videos:
            video_record = videos[0]

            video = self.parser.parse_single_video(video_record)
            video.update(self.parser.parse_video_meta(video_record))

            return video

        raise PyTubeNotFoundException('Video cannot be found')

    def get_videos_for(self, identifier, **kwargs):
        """
        Retrieves a list of videos belonging to the specified user or channel, which is constructed via a number of
        Youtube Data API calls.
        If username is not valid, it raises PyTubeNotFound
        """

        mock_requests = kwargs.get('mocks', {})

        if not identifier:
            raise PyTubeNotFoundException(u'You must specify a username')

        channels = self._get_channels_for(identifier)

        if channels:
            playlist_id = channels[0].get('contentDetails', {}).get('relatedPlaylists', {}).get('uploads')
            if not playlist_id:
                raise PyTubeNotFoundException(u'Could not find the "uploads" playlist for {}'.format(identifier))

            playlist_items = self._get_playlist_items_for_playlist(playlist_id,
                                                                   http_mock=mock_requests.get('playlistItems'))

            if playlist_items:
                video_meta = self._get_video_meta_for_videos(playlist_items, http_mock=mock_requests.get('videos'))
                return self.parser.parse_videos(identifier, playlist_items, video_meta)
            return None

        else:
            raise PyTubeNotFoundException(u'User {} not found'.format(identifier))

    def _get_channels_for(self, identifier):
        """
        Retrieves the channel information for a given identifier. It will return some basic user information
        such as title and description (amongst others), but also returns the playlist ids belonging to that user
        """
        try:
            criteria = {
                'part': 'contentDetails'
            }

            if self.is_channel_id(identifier):
                criteria['id'] = identifier
            else:
                criteria['forUsername'] = identifier

            channels_response = self.youtube_client.channels().list(**criteria).execute(http=self.http_mock)
        except HttpError:
            raise PyTubeNotFoundException(u'Channel for {} cannot be found'.format(identifier))

        return channels_response.get('items', [])

    def _get_playlist_items_for_playlist(self, playlist_id, results_per_page=50, page_token=None, http_mock=None):
        """
        Retrieves a list of videos which belong to a playlist. The data returned in this response includes video title,
        description, thumbnails and video id
        :param playlist_id: id of the playlist to retrieve videos for
        :param results_per_page: number of results to return per request
        :param page_token: the token to retrieve subsequent pages of data
        :param http_mock: HttpMock object used within unit testing to mock the API response
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
            raise PyTubeNotFoundException('Playlist with id {} cannot be found'.format(playlist_id))

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
            raise PyTubeNotFoundException('Videos cannot be found {}'.format(playlist_items))

        data = {}

        for video in video_response.get('items', []):
            data[video['id']] = video

        return data
