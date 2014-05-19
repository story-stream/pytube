from lxml import etree
from dateutil.parser import parse as date_parser

class YoutubeParser(object):
    __namespaces = {'a': 'http://www.w3.org/2005/Atom',
                    'app': 'http://www.w3.org/2007/app',
                    'batch': 'http://schemas.google.com/gdata/batch',
                    'gd': 'http://schemas.google.com/g/2005',
                    'georss': 'http://www.georss.org/georss',
                    'gml': 'http://www.opengis.net/gml',
                    'media': 'http://search.yahoo.com/mrss/',
                    'openSearch': 'http://a9.com/-/spec/opensearch/1.1/',
                    'yt': 'http://gdata.youtube.com/schemas/2007'}

    __entity_xpath = [
        {'name': 'id', 'xpath': 'a:id/text()'},
        {'name': 'published', 'xpath': 'a:published/text()', 'convert': date_parser},
        {'name': 'updated', 'xpath': 'a:updated/text()', 'convert': date_parser},
        {'name': 'title', 'xpath': 'a:title/text()'},
        {'name': 'content', 'xpath': 'a:content/text()'}
    ]

    def get_entries(self, xml):
        root = etree.fromstring(xml)

        return [self._parse_entry(entry) for entry in root.xpath('//a:entry', namespaces=self.__namespaces)]

    def _parse_entry(self, entry):
        obj = {}
        for prop_map in self.__entity_xpath:
            value = entry.xpath(prop_map['xpath'], namespaces=self.__namespaces)[0]

            if prop_map.get('convert'):
                obj[prop_map['name']] = prop_map.get('convert')(value)
            else:
                obj[prop_map['name']] = value

        return obj






