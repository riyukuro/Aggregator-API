import requests_cache as rc
from requests import exceptions
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from webdriver_manager.firefox import GeckoDriverManager

HEADER = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

class driver:
    def __init__(self):
        self.session = rc.CachedSession()
        self.executable = GeckoDriverManager().install()


    def get(self, url: str, headless=True, js=False):
        if js is not True and headless is True:
            for i in range(3):
                try: req = self.session.get(url, headers=HEADER)
                except exceptions.RequestException as e:
                    if i >= 3: return e
                return req

        else:
            #TODO: Implement log checking for status codes.
            firefoxOptions = webdriver.FirefoxOptions()
            firefoxOptions.headless = headless
            caps = DesiredCapabilities().FIREFOX
            caps["pageLoadStrategy"] = "eager"
            #caps["loggingPrefs"] = {'browser': 'ALL'}
            self.browser = webdriver.Firefox(executable_path=self.executable, options=firefoxOptions, capabilities=caps)
            self.browser.get(url)
            
            return self.browser


    def close(self):
        return self.browser.close()
        

from importlib import import_module
def server_import(source): 
    return getattr(import_module('sources.' + source), source)()
