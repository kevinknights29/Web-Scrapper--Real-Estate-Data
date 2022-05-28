import requests
from lxml import html
from common import config


class Homepage:
    def __init__(self, site_id, url):
        self._config = config()['sites'][site_id]
        self._queries = self._config['queries']
        self._html = None
        self._visit(url)

    @property
    def listing_links(self):
        links = []
        for link in self._select(self._queries['listing_links']):
            if link:
                links.append(str(link))
        return set(links)

    def _select(self, query):
        return self._html.xpath(query)

    def _visit(self, url):
        response = requests.get(url)
        response.raise_for_status()
        response = response.content.decode(encoding='utf-8')
        self._html = html.fromstring(html=response)
