from collections import OrderedDict
from lxml import etree
from dateutil.parser import parse as date_parser


class YoutubeParser(object):
    _namespaces = {'a': 'http://www.w3.org/2005/Atom',
                   'app': 'http://www.w3.org/2007/app',
                   'batch': 'http://schemas.google.com/gdata/batch',
                   'gd': 'http://schemas.google.com/g/2005',
                   'georss': 'http://www.georss.org/georss',
                   'gml': 'http://www.opengis.net/gml',
                   'media': 'http://search.yahoo.com/mrss/',
                   'openSearch': 'http://a9.com/-/spec/opensearch/1.1/',
                   'yt': 'http://gdata.youtube.com/schemas/2007'}

    __entity_xpath = [
        {'name': 'id', 'xpath': 'media:group/yt:videoid/text()'},
        {'name': 'published', 'xpath': 'a:published/text()', 'convert': date_parser},
        {'name': 'updated', 'xpath': 'a:updated/text()', 'convert': date_parser},
        {'name': 'title', 'xpath': 'a:title/text()'},
        {'name': 'description', 'xpath': 'media:group/media:description/text()'},
        {'name': 'author_name', 'xpath': 'a:author/a:name/text()'},
        {'name': 'author_url', 'xpath': 'a:author/a:uri/text()'},
        {'name': 'user_name', 'xpath': 'a:author/a:uri/text()', 'convert': lambda x: x[x.rfind('/')+1:]},
        {'name': 'video_url', 'xpath': 'media:group/media:content[@isDefault]/@url'},
        {'name': 'keywords', 'xpath': 'media:group/media:keywords/text()'},
        {'name': 'comments', 'children': [
            {'name': 'count', 'xpath': 'gd:comments/gd:feedLink/@countHint'},
            {'name': 'href', 'xpath': 'gd:comments/gd:feedLink/@href'}
        ]},
        {'name': 'rating', 'children': [
            {'name': 'average', 'xpath': 'gd:rating/@average'},
            {'name': 'total', 'xpath': 'gd:rating/@numRaters'},
            {'name': 'likes', 'xpath': 'yt:rating/@numLikes'},
            {'name': 'dislikes', 'xpath': 'yt:rating/@numDislikes'},
        ]},
        {'name': 'statistics', 'children': [
            {'name': 'favourites', 'xpath': 'yt:statistics/@favoriteCount'},
            {'name': 'views', 'xpath': 'yt:statistics/@viewCount'}
        ]},
        {'name': 'geolocation', 'xpath': 'georss:where/gml:Point/gml:pos/text()'},
        {'name': 'thumbnails', 'multi': True, 'xpath': 'media:group/media:thumbnail', 'convert': lambda x: [e.attrib for e in x]}
    ]

    def get_entries(self, xml):
        root = etree.fromstring(xml)

        return [self._parse_entry(entry) for entry in root.xpath('//a:entry', namespaces=self._namespaces)]

    def get_video(self, xml):
        root = etree.fromstring(xml)

        return self._parse_entry(root.xpath('//a:entry', namespaces=self._namespaces)[0])

    def _parse_entry(self, entry):
        return self.__parse_mapping(entry, self.__entity_xpath)

    def __parse_mapping(self, entry, collection):
        obj = OrderedDict()

        for prop_map in collection:
            if 'children' in prop_map:
                obj[prop_map['name']] = self.__parse_mapping(entry, prop_map['children'])
            else:
                try:
                    result = entry.xpath(prop_map['xpath'], namespaces=self._namespaces)

                    if prop_map.get('multi', False):
                        value = result
                    else:
                        try:
                            value = result[0]
                        except:
                            obj[prop_map['name']] = None
                            continue

                    if prop_map.get('convert'):
                        obj[prop_map['name']] = prop_map.get('convert')(value)
                    else:
                        obj[prop_map['name']] = value
                except:
                    obj[prop_map['name']] = None

        return obj






