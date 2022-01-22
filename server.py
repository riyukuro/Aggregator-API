import requests_cache as rc
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

HEADER = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
session = rc.CachedSession()

class driver:
    def get(self, url: str, headless=True, js=False):
        if js is not True and headless is True:
            #session = rc.CachedSession()
            return session.get(url, headers=HEADER)

        else:
            firefoxOptions = webdriver.FirefoxOptions()
            firefoxOptions.headless = headless
            caps = DesiredCapabilities().FIREFOX
            caps["pageLoadStrategy"] = "eager"

            self.browser = webdriver.Firefox(options=firefoxOptions)
            self.browser.get(url)

            return self.browser

    def close(self):
        return self.browser.close()