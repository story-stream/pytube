#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import json
from unittest import TestCase
import datetime
from dateutil.tz import tzutc
from pytube.parser import PyTubeParser


class ParserTestCase(TestCase):
    def setUp(self):
        self.parser = PyTubeParser()
        self.username = 'porsche'

    def test_can_parse_playlist_item(self):
        json_data = self.__load_json_file('video_parser.json')

        parsed_video = self.parser.parse_playlist_item(self.username, json_data['snippet'])

        self.assertEqual(parsed_video['id'], u'EyykDmuCxZo')
        self.assertEqual(parsed_video['published'], datetime.datetime(2015, 3, 17, 10, 18, 33, tzinfo=tzutc()))
        self.assertEqual(parsed_video['title'], u'Behind the wheel of the Cayman GT4 with Walter Röhrl')
        self.assertTrue(len(parsed_video['description']) > 10)
        self.assertEqual(parsed_video['author_name'], u'Porsche')
        self.assertEqual(parsed_video['author_url'], u'http://www.youtube.com/v/porsche')
        self.assertEqual(parsed_video['user_name'], u'porsche')
        self.assertEqual(parsed_video['video_url'], u'http://www.youtube.com/v/EyykDmuCxZo')

    def test_can_parse_video_meta_without_recording_details(self):
        data = {
            "kind": "youtube#video",
            "etag": "\"9iWEWaGPvvCMMVNTPHF9GiusHJA/CgbPLC3YustFNvpRTe3ysq7iE9g\"",
            "id": "6oQRq94Cntw",
            "statistics": {
                "viewCount": "24059",
                "likeCount": "505",
                "dislikeCount": "6",
                "favoriteCount": "0",
                "commentCount": "81"
            }
        }

        parsed_meta_data = self.parser.parse_video_meta(data)

        self.assertEqual(int(parsed_meta_data['rating']['likes']), 505)
        self.assertEqual(int(parsed_meta_data['comments']['count']), 81)
        self.assertEqual(int(parsed_meta_data['statistics']['views']), 24059)
        self.assertIsNone(parsed_meta_data['geolocation'])

    def test_can_parse_video_meta_with_recording_details(self):
        data = {
            "kind": "youtube#video",
            "etag": "\"9iWEWaGPvvCMMVNTPHF9GiusHJA/mDdeYuKp4fX16c-CyGAW2p2SVTU\"",
            "id": "EyykDmuCxZo",
            "statistics": {
                "viewCount": "59940",
                "likeCount": "329",
                "dislikeCount": "4",
                "favoriteCount": "0",
                "commentCount": "46"
            },
            "recordingDetails": {
                "locationDescription": "Geneva",
                "location": {
                    "latitude": -157.87353515625,
                    "longitude": 21.37124437061831,
                    "altitude": 0.0
                },
                "recordingDate": "2015-03-16T09:36:37.000Z"
            }
        }

        parsed_meta_data = self.parser.parse_video_meta(data)

        self.assertEqual(int(parsed_meta_data['rating']['likes']), 329)
        self.assertEqual(int(parsed_meta_data['comments']['count']), 46)
        self.assertEqual(int(parsed_meta_data['statistics']['views']), 59940)
        self.assertIsNotNone(parsed_meta_data['geolocation'])
        self.assertEqual(parsed_meta_data['geolocation']['latitude'], -157.87353515625)
        self.assertEqual(parsed_meta_data['geolocation']['longitude'], 21.37124437061831)

    def test_can_merge_playlistitems_and_video_meta_when_all_complete(self):
        playlist_items = [item['snippet'] for item in self.__load_json_file('playlistitems.json').get('items')]
        video_meta = {video['id']: video for video in self.__load_json_file('videos.json').get('items')}

        parsed_videos = self.parser.parse_videos('porsche', playlist_items, video_meta)

        self.assertEqual(len(parsed_videos), 10)

        for video in parsed_videos:
            self.assertIsNotNone(video['id'])
            self.assertIsNotNone(video['rating'])
            self.assertIsNotNone(video['comments'])
            self.assertIsNotNone(video['statistics'])

    def test_can_merge_playlistitems_and_video_meta_when_video_meta_incomplete(self):
        playlist_items = [item['snippet'] for item in self.__load_json_file('playlistitems.json').get('items')]
        video_meta = {video['id']: video for video in self.__load_json_file('videos.json').get('items')[1:]}

        parsed_videos = self.parser.parse_videos('porsche', playlist_items, video_meta)

        self.assertEqual(len(parsed_videos), 10)

        for video in parsed_videos:
            self.assertIsNotNone(video['id'])
            self.assertIsNotNone(video['rating'])
            self.assertIsNotNone(video['comments'])
            self.assertIsNotNone(video['statistics'])

    def __load_json_file(self, fixture_name):
        import os

        path = os.path.dirname(__file__)
        fixture_path = os.path.join(path, 'fixtures', fixture_name)

        with open(fixture_path, 'r') as fp:
            data = json.load(fp)

        return data