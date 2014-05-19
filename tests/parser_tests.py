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
        from lxml import etree

        xml_entry = etree.fromstring(open(os.path.join(os.path.dirname(__file__), 'entry.xml'), 'r').read())[0]
        parsed_entry = self.parser._parse_entry(xml_entry)

        self.assertEqual(parsed_entry['id'], 'http://gdata.youtube.com/feeds/api/videos/0zDDEvROU48')

        self.assertEqual(parsed_entry['updated'].month, 5)