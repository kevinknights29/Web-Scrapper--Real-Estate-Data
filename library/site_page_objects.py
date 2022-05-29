import requests
from lxml import html
from common import config


class ListingsPage():
    def __init__(self, site_id, url):
        self._config = config()['sites'][site_id]
        self._queries = self._config['queries']
        self._html = None
        self._url = url
        self._visit(self._url)

    def _select(self, queries):
        if type(queries) == list and len(queries) > 1:
            for query in queries:
                result = self._html.xpath(query)
                if result:
                    return result
        else:
            return self._html.xpath(queries)

    def _visit(self, url):
        response = requests.get(url)
        response.raise_for_status()
        response = response.content.decode(encoding='utf-8')
        self._html = html.fromstring(html=response)

    def _get_next_page(self):
        result = self._select(self._queries['next_page'])
        if type(result) == list and len(result) > 1:
            return result[0]
        else:
            return result if result else ''


class Homepage(ListingsPage):
    def __init__(self, site_id, url):
        super().__init__(site_id, url)

    @property
    def listing_links(self):
        links = []
        for link in self._select(self._queries['listing_links']):
            if link:
                links.append(str(link))
        return set(links)


class ItemPage(ListingsPage):
    def __init__(self, site_id, url):
        super().__init__(site_id, url)

    @property
    def title(self):
        result = self._select(self._queries['listing_title'])
        if result and type(result) == list:
            return result[0]
        else:
            return result if result else ''

    @property
    def price(self):
        result = self._select(self._queries['listing_price'])
        if result and type(result) == list:
            return result[0]
        else:
            return result if result else ''

    @property
    def description(self):
        result = self._select(self._queries['listing_description'])
        if result and type(result) == list:
            return ' '.join(result)
        else:
            return result if result else ''

    @property
    def url(self):
        result = self._url
        return result if result else ''
