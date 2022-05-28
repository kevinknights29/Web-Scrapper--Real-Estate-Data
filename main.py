import argparse
import logging
from common import config
import site_page_objects as sites
logging.basicConfig(level=logging.INFO)


logger = logging.getLogger(__name__)


def _site_scraper(site_id):
    host = config()['sites'][site_id]['url']
    logging.info(f'Now scraping: {host}')
    homepage = sites.Homepage(site_id, url=host)

    for link in homepage.listing_links:
        print(link)


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
