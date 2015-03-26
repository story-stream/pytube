from dateutil.parser import parse as date_parser


class PyTubeParser(object):
    def parse_videos(self, username, playlist_items, video_meta):
        videos = []

        for playlist_item in playlist_items:
            video = self.parse_playlist_item(username, playlist_item)
            meta_for_video = video_meta.get(video['id'], {})

            video.update(self.parse_video_meta(meta_for_video))

            videos.append(video)

        return videos

    def parse_playlist_item(self, username, data):
        video_id = data["resourceId"]["videoId"]
        return {
            u'id': video_id,
            u'published': date_parser(data["publishedAt"]),
            u'title': data["title"],
            u'description': data["description"],
            u'author_name': data["channelTitle"],
            u'author_url': u'http://www.youtube.com/v/{}'.format(username),
            u'user_name': username,
            u'video_url': u'http://www.youtube.com/v/{}'.format(video_id),
            u'thumbnails': data.get('thumbnails', []),
            u'keywords': []  # doesnt appear to return this any more
        }

    def parse_video_meta(self, meta):
        statistics = meta.get('statistics', {})
        geo_location = meta.get('recordingDetails')

        if geo_location and geo_location.get('location'):
            geo_location = geo_location.get('location', None)

        return {
            u'rating': {u'likes': statistics.get('likeCount', 0) or 0},
            u'statistics': {
                u'views': statistics.get('viewCount', 0) or 0,
                u'favourites': statistics.get('favoriteCount', 0) or 0
            },
            u'comments': {u'count': statistics.get('commentCount', 0) or 0},
            u'geolocation': geo_location
        }
