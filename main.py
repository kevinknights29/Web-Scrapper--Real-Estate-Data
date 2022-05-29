import re
import argparse
import logging
from urllib.error import HTTPError
from common import config
import site_page_objects as sites
logging.basicConfig(level=logging.INFO)


logger = logging.getLogger(__name__)
is_well_formed_url = re.compile(r'^https?://.+/.+$')
is_root_path = re.compile(r'^/.+$')


def _site_scraper(site_id):
    domain = config()['sites'][site_id]['domain']
    host = config()['sites'][site_id]['url']
    logging.info(f'Now scraping: {host}')
    homepage = sites.Homepage(site_id, url=host)

    items = []
    for link in homepage.listing_links:
        item = _fetch_item(site_id, domain, link)
        if item:
            logger.info('Item fetched succesfully!')
            items.append(item)
    logger.info(f'Items fetched: {len(items)} / {len(homepage.listing_links)}')


def _fetch_item(site_id, host, link):
    logger.info(f'Fetching item from {_build_link(host, link)}')
    item = None
    try:
        item = sites.ItemPage(site_id, url=_build_link(host, link))
    except (HTTPError, MaxRetryError) as e:
        logger.warning('Error while fetching the item', exc_info=False)

    condition = not item.price or not item.title
    if item and condition:
        logger.warning('Invalid item. There is no title or price!')
        return None
    return item


def _build_link(host, link):
    if is_well_formed_url.match(link):
        return link
    elif is_root_path.match(link):
        return f'{host}{link}'
    else:
        return f'{host}/{link}'


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    site_choices = list(config()['sites'].keys())
    parser.add_argument(
        'site',
        help='The site you would like to scrape',
        type=str,
        choices=site_choices
    )
    args = parser.parse_args()
    _site_scraper(args.site)
