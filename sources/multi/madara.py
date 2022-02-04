from server import driver
from bs4 import BeautifulSoup as bs
from data import formatting

class madara:
    source_name: str = None
    base_url: str = None
    latest_slug: str = None
    popular_slug: str = None

    browser = driver()
    print('Madara', base_url)

    def fetch_latest(self):
        latest = list()
        #req = bs(self.browser.get(self.base_url))
        return [self.base_url]