from bs4 import BeautifulSoup as bs
import requests as r
from selenium import webdriver

header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

source_name = 'mangago'
base_url = 'https://www.mangago.me'


def fetch_latest():
    latest_data = list()
    latest_url = f'{base_url}/list/latest/all/1/'

    req = bs(r.get(latest_url, headers=header).text, 'html.parser')
    for i in req.select_one('#search_list').find_all('li'):
        title = i.select_one('div > div > div > span > h2 > a').get_text()
        url = '/' +i.select_one('div > div > div > span > h2 > a')['href'].lstrip(base_url)
        structure = {'manga_title': title, 'manga_url': url}
        latest_data.append(structure)

    return {source_name: latest_data}


def fetch_popular():
    popular_url = f'{base_url}/genre/all/1/?f=1&o=1&sortby=view&e='
    popular_data = list()
    
    req = bs(r.get(popular_url, headers=header).text, 'html.parser')
    for i in req.select('div.flex1'):
        url = i.a['href'].lstrip(base_url)
        title = i.span.get_text()
        cover_url = i.img['data-src']
        structure = {'manga_title': title, 'manga_url': url, 'manga_cover': cover_url}
        popular_data.append(structure)

    return {source_name: popular_data}


def fetch_search(search):
    req = bs(r.get(f'{base_url}/r/l_search/?name={search}', headers=header).text, 'html.parser')
    data = list()
    for i in req.select_one('#search_list').find_all('li'):
        title = i.a['title']
        url = i.a['href'].strip(base_url)
        structure = {'manga_name': title, 'manga_url': url}
        data.append(structure)
    return data


def fetch_manga(manga_slug):
    data = list()

    req = bs(r.get(base_url + manga_slug, headers=header).text, 'html.parser')
    for i in req.select_one('#chapter_table > tbody:nth-child(1)').find_all('tr'):
        chapter_title = i.select_one('i > b')
        chapter_url = i.a['href'].lstrip(base_url)
        structure = {'chapter_title': chapter_title,'chapter_url': chapter_url}
        data.append(structure)
        
    return data


def fetch_pages(chapter_slug):
    page_urls = list()
    data = list()

    fireFoxOptions = webdriver.FirefoxOptions()
    fireFoxOptions.headless = True
    brower = webdriver.Firefox(options=fireFoxOptions)

    brower.get(f'{base_url}/{chapter_slug}')
    req = bs(brower.page_source, 'html.parser')
    for i in req.select_one('#dropdown-menu-page').find_all('li'):
        url = i.a['href']
        page_urls.append(url)

    for i in page_urls:
        brower.get(base_url + i)
        #page_req = bs(r.get(base_url + i, headers=header).text, 'html.parser')
        page_req = bs(brower.page_source, 'html.parser')
        #print(page_req)
        data.append(page_req.select_one('img')['src'])
    brower.quit()

    return data