import argparse
import csv
import logging
import os
import re
from datetime import datetime
from urllib.error import HTTPError

from urllib3.exceptions import MaxRetryError

import site_page_objects as sites
from common import config

logging.basicConfig(level=logging.INFO)


logger = logging.getLogger(__name__)
is_well_formed_url = re.compile(r'^https?://.+/.+$')
is_root_path = re.compile(r'^/.+$')


def _site_scraper(site_id, max_pages):
    domain = config()['sites'][site_id]['domain']
    host = config()['sites'][site_id]['url']
    logging.info(f'Now scraping: {host}')
    homepage = sites.Homepage(site_id, url=host)

    items = []
    _get_items_from_links(items, site_id, domain,
                          links=homepage.listing_links)

    page_count = 1
    while True and page_count < max_pages:
        message = f'Items fetched: {len(items)}' + \
            ' || ' + f'From Pages: {page_count}'
        logger.info(message)

        if homepage._get_next_page():
            logger.info(f'Next page: {homepage._get_next_page()}')
            next_page_url = _build_link(domain, link=homepage._get_next_page())
            homepage = sites.Homepage(site_id, url=next_page_url)
            _get_items_from_links(items, site_id, domain,
                                  links=homepage.listing_links)
            page_count += 1
        else:
            break

    logger.info('Scraping completed!')
    _save_items(site_id, items)


def _save_items(site_id, items):
    now = datetime.now().strftime('%Y_%m_%d')
    output_file_name = f'./output/{site_id}_{now}_items.csv'
    csv_headers = list(
        filter(
            lambda prop: not prop.startswith('_'),
            dir(items[0])
        )
    )

    with open(output_file_name, mode='w+', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(csv_headers)

        for item in items:
            row = [str(getattr(item, prop)) for prop in csv_headers]
            writer.writerow(row)

    logging.info(
        f'Items stored succesfully at: {os.path.relpath(output_file_name)}')


def _get_items_from_links(items, site_id, domain, links):
    if items is None:
        items = []

    for link in links:
        item = _fetch_item(site_id, domain, link)
        if item:
            logger.info('Item fetched succesfully!')
            items.append(item)


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
        choices=site_choices,
    )
    parser.add_argument(
        'max_pages',
        help='The max number of pages you would like to scrape. (default: 10000)',
        type=int,
        nargs='?',
        const=10000
    )
    args = parser.parse_args()
    _site_scraper(args.site, args.max_pages)
