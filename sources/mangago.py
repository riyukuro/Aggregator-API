from bs4 import BeautifulSoup as bs
import requests as r
from selenium import webdriver

header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

source_name = 'mangago'
base_url = 'https://www.mangago.me'


def fetch_latest():
    latest_url = f'{base_url}/genre/all/1/?f=1&o=1&sortby=update_date&e='
    latest_data = list()
    
    req = bs(r.get(latest_url, headers=header).text, 'html.parser')
    for i in req.select('div.flex1'):
        title = i.span.get_text()
        url = '/' +i.a['href'].lstrip(base_url)
        cover_url = i.img['data-src']
        structure = {'manga_title': title, 'manga_url': url, 'manga_cover': cover_url}
        latest_data.append(structure)

    return {source_name: latest_data}


def fetch_popular():
    popular_url = f'{base_url}/genre/all/1/?f=1&o=1&sortby=view&e='
    popular_data = list()
    
    req = bs(r.get(popular_url, headers=header).text, 'html.parser')
    for i in req.select('div.flex1'):
        title = i.span.get_text()
        url = '/' +i.a['href'].lstrip(base_url)
        cover_url = i.img['data-src']
        structure = {'manga_title': title, 'manga_url': url, 'manga_cover': cover_url}
        popular_data.append(structure)

    return {source_name: popular_data}


def fetch_search(search):
    req = bs(r.get(f'{base_url}/r/l_search/?name={search}', headers=header).text, 'html.parser')
    search_data = list()
    for i in req.select_one('#search_list').find_all('li'):
        title = i.a['title']
        url = '/' + i.a['href'].lstrip(base_url)
        cover_url = i.a.img['src']
        structure = {'manga_title': title, 'manga_url': url, 'manga_cover': cover_url}
        search_data.append(structure)
    return {source_name: search_data}


def fetch_manga(manga_slug):
    manga_url = base_url + manga_slug
    req = bs(r.get(manga_url, headers=header).text, 'html.parser')

    title = req.select_one('.w-title > h1').get_text().strip()
    cover = req.select_one('.cover > img')['src']
    desc = req.select_one('div.manga_summary').get_text().strip()
    
    status = req.select_one('table.left > tbody > tr > td > span:nth-child(2)').get_text().lower()
    author = ''
    artist = ''
    genres = []
    for i in req.select_one('table.left > tbody:nth-child(1) > tr:nth-child(3) > td:nth-child(1)').find_all('a'):
        genres.append(i.get_text())
        

    chapters = list()
    for i in req.select_one('#chapter_table > tbody').find_all('tr'):
        chapter_title = " ".join(i.select_one('a').get_text().strip().split())
        chapter_url = '/' +i.a['href'].lstrip(base_url)
        chapter_structure = {'chapter_title': chapter_title,'chapter_url': chapter_url}
        chapters.append(chapter_structure)
    chapters.reverse()

    structure = {"manga_title": title, "manga_cover": cover, "manga_desc": desc, "manga_status": status, "manga_author": author, "manga_artist": artist, "manga_genres": genres, "manga_chapters": chapters}
    return {source_name: structure}


def fetch_pages(chapter_slug):
    page_urls = list()
    data = list()

    fireFoxOptions = webdriver.FirefoxOptions()
    fireFoxOptions.headless = True
    brower = webdriver.Firefox(options=fireFoxOptions)

    brower.get(f'{base_url}{chapter_slug}')
    req = bs(brower.page_source, 'html.parser')
    for i in req.select_one('#dropdown-menu-page').find_all('li'):
        url = i.a['href']
        page_urls.append(url)

    for i in page_urls:
        brower.get(base_url + i)
        page_req = bs(brower.page_source, 'html.parser')
        data.append(page_req.select_one('img')['src'])
    brower.quit()

    return data