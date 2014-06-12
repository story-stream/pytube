import os
import unittest
from pytube.parser import YoutubeParser


class ParserTestCase(unittest.TestCase):

    def setUp(self):
        self.xml = open(os.path.join(os.path.dirname(__file__), 'feed.xml'), 'r').read()
        self.parser = YoutubeParser()

    def test_parser_has_items(self):

        entries = self.parser.get_entries(self.xml)

        self.assertEqual(len(entries), 25)

    def test_parse_entry_geo(self):
        parsed_entry = self.parser.get_video(open(os.path.join(os.path.dirname(__file__), 'entry.xml'), 'r').read())

        self.assertEqual(parsed_entry['id'], 'maA1wGBX7ag')

        self.assertEqual(parsed_entry['updated'].month, 6)
        self.assertEqual(parsed_entry['author_name'], 'Ola Englund')
        self.assertEqual(parsed_entry['user_name'], 'fearedse')
        self.assertEqual(parsed_entry['comments']['count'], '357')
        self.assertEquals(parsed_entry['rating']['average'], '4.9704895')
        self.assertEquals(parsed_entry['rating']['total'], '1491')
        self.assertEquals(parsed_entry['statistics']['favourites'], '0')
        self.assertEquals(parsed_entry['statistics']['views'], '87300')
        self.assertEquals(parsed_entry.get('keywords'), None)

        self.assertEqual(len(parsed_entry['thumbnails']), 7)
        self.assertNotEqual(parsed_entry['description'], '')
        self.assertEquals(parsed_entry['geolocation'], '21.37124437061831 -157.87353515625')

        self.assertEqual(parsed_entry['thumbnails'][0]['url'], 'https://i1.ytimg.com/vi/maA1wGBX7ag/default.jpg')

    def test_parse_no_geo(self):
        parsed_entry = self.parser.get_video(open(os.path.join(os.path.dirname(__file__), 'entry-no-geo.xml'), 'r').read())

        self.assertEquals(parsed_entry.get('geolocation'), None)