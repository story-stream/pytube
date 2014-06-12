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

    def test_parse_entry(self):
        parsed_entry = self.parser.get_video(open(os.path.join(os.path.dirname(__file__), 'entry.xml'), 'r').read())

        self.assertEqual(parsed_entry['id'], 'maA1wGBX7ag')

        self.assertEqual(parsed_entry['updated'].month, 6)
        self.assertEqual(parsed_entry['author_name'], 'Ola Englund')
        self.assertEqual(parsed_entry['user_name'], 'fearedse')
        self.assertEqual(parsed_entry['comments']['count'], '357')

        self.assertEqual(len(parsed_entry['thumbnails']), 7)
        self.assertNotEqual(parsed_entry['description'], '')

        self.assertEqual(parsed_entry['thumbnails'][0]['url'], 'https://i1.ytimg.com/vi/maA1wGBX7ag/default.jpg')