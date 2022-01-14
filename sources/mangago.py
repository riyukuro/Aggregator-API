from bs4 import BeautifulSoup as bs
import requests as r
from selenium import webdriver
from constants import HEADER
from data import LPR, MANGA
from dataclasses import asdict

import requests_cache as rc

source_name = 'mangago'
base_url = 'https://www.mangago.me'
latest_url = f'{base_url}/genre/all/1/?f=1&o=1&sortby=update_date&e='
popular_url = f'{base_url}/genre/all/1/?f=1&o=1&sortby=view&e='

session = rc.CachedSession()

def fetch_latest():
    latest_data = list()
    req = bs(session.get(latest_url, headers=HEADER).text, 'html.parser')
    for i in req.select('div.flex1'):
        data = LPR(
            source=source_name,
            manga_title=i.span.get_text(),
            manga_slug='/' + i.a['href'].lstrip(base_url),
            manga_cover=i.img['data-src']
        )

        latest_data.append(asdict(data))

    return latest_data


def fetch_popular():
    popular_data = list()
    req = bs(session.get(popular_url, headers=HEADER).text, 'html.parser')
    for i in req.select('div.flex1'):
        data = LPR(
            source=source_name,
            manga_title=i.span.get_text(),
            manga_slug='/' + i.a['href'].lstrip(base_url),
            manga_cover=i.img['data-src']
        )
        
        popular_data.append(asdict(data))

    return popular_data


def fetch_search(search):
    req = bs(session.get(f'{base_url}/r/l_search/?name={search}', headers=HEADER).text, 'html.parser')
    search_data = list()
    for i in req.select_one('#search_list').find_all('li'):
        data = LPR(
            source=source_name,
            manga_title=i.a['title'],
            manga_slug='/' + i.a['href'].lstrip(base_url),
            manga_cover=i.a.img['src']
        )

        search_data.append(asdict(data))

    return search_data


def fetch_manga(manga_slug):
    manga_url = base_url + manga_slug
    req = bs(session.get(manga_url, headers=HEADER).text, 'html.parser')

    title = req.select_one('.w-title > h1').get_text().strip()
    cover = req.select_one('.cover > img')['src']
    desc = req.select_one('div.manga_summary').get_text().strip().replace('\t', '').replace('\n', '')
    status = req.select_one('table.left > tbody > tr > td > span:nth-child(2)').get_text().lower()
    author = ''
    artist = ''
    genres = list()
    for i in req.select_one('table.left > tbody:nth-child(1) > tr:nth-child(3) > td:nth-child(1)').find_all('a'):
        genres.append(i.get_text())
        
    chapters = list()
    for i in req.select_one('#chapter_table > tbody').find_all('tr'):
        chapter_title = " ".join(i.select_one('a').get_text().strip().split())
        chapter_url = '/' + i.a['href'].lstrip(base_url)
        chapter_structure = {'chapter_title': chapter_title,'chapter_slug': chapter_url}
        chapters.append(chapter_structure)
    chapters.reverse()

    data = MANGA(
        source=source_name,
        manga_title=title,
        manga_cover=cover,
        manga_desc=desc,
        manga_status=status,
        manga_author=author,
        manga_artist=artist,
        manga_genres=genres,
        manga_chapters=chapters
    )

    return asdict(data)


def fetch_pages(chapter_slug):
    page_urls = list()
    image_urls = list()

    fireFoxOptions = webdriver.FirefoxOptions()
    fireFoxOptions.headless = True
    browser = webdriver.Firefox(options=fireFoxOptions)

    browser.get(f'{base_url}{chapter_slug}')
    req = bs(browser.page_source, 'html.parser')
    for i in req.select_one('#dropdown-menu-page').find_all('li'):
        url = i.a['href']
        page_urls.append(url)

    for i in page_urls:
        browser.get(base_url + i)
        page_req = bs(browser.page_source, 'html.parser')
        image_urls.append(page_req.select_one('img')['src'])
    browser.quit()

    return image_urls
