from server import driver
from bs4 import BeautifulSoup as bs
from data import LPR, MANGA, CHAPTER
import re

source_name = 'mangago'
base_url = 'https://www.mangago.me'
latest_url = f'{base_url}/genre/all/1/?f=1&o=1&sortby=update_date&e='
popular_url = f'{base_url}/genre/all/1/?f=1&o=1&sortby=view&e='

browser = driver()

def fetch_latest():
    latest_data = list()
    req = bs(browser.get(latest_url).text, 'html.parser')
    for i in req.select('div.flex1'):
        data = LPR(
            source=source_name,
            manga_title=i.span.get_text(),
            manga_slug='/' + i.a['href'].lstrip(base_url),
            manga_cover=i.img['data-src']
        ).format()

        latest_data.append(data)

    return latest_data


def fetch_popular():
    popular_data = list()
    req = bs(browser.get(popular_url).text, 'html.parser')
    for i in req.select('div.flex1'):
        data = LPR(
            source=source_name,
            manga_title=i.span.get_text(),
            manga_slug='/' + i.a['href'].lstrip(base_url),
            manga_cover=i.img['data-src']
        ).format()

        popular_data.append(data)

    return popular_data


def fetch_search(search):
    req = bs(browser.get(f'{base_url}/r/l_search/?name={search}').text, 'html.parser')
    search_data = list()
    for i in req.select_one('#search_list').find_all('li'):
        data = LPR(
            source=source_name,
            manga_title=i.a['title'],
            manga_slug='/' + i.a['href'].lstrip(base_url),
            manga_cover=i.a.img['src']
        ).format()
        
        search_data.append(data)

    return search_data


def fetch_manga(manga_slug):
    manga_url = base_url + manga_slug
    req = bs(browser.get(manga_url).text, 'html.parser')

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
        chapter = CHAPTER(
            source = source_name,
            chapter_title = " ".join(i.select_one('a').get_text().strip().split()),
            chapter_slug = '/' + i.a['href'].lstrip(base_url),
        ).format()
        chapters.append(chapter)

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
    ).format()

    return data


def fetch_pages(chapter_slug):

    page_urls = list()
    #image_urls = list()

    req = bs(browser.get(f'{base_url}{chapter_slug}', js=True).page_source, 'html.parser')
    for i in req.select_one('#dropdown-menu-page').find_all('li'):
        url = i.a['href']
        page_urls.append(url)
        print(url)

    """
    for i, x in enumerate(page_urls):
        page_req = bs(browser1.browser("headed", f'{base_url}{x}', js=True), 'html.parser')
        img = page_req.find('img', id=f'page{i+1}')

        if img is None:
            #not sure if this works on all canvas but for now w.e
            manga_title = chapter_slug.split('/')[2]
            chapter = re.findall('[0-9]+', page_req.select_one('div >  h3> span:nth-child(3)').get_text())
            img = f'https://iweb7.mangapicgallery.com/imgfiles/{manga_title}/{chapter[0]}/00{i}.png'

        image_urls.append(img)
    """

    browser.close()
    return page_urls

def fetch_page(page_slug):
    

    page_req = bs(browser.get(f'{base_url}{page_slug}', js=True).page_source, 'html.parser')
    page = re.findall('[0-9]+', page_req.select_one('a.page').get_text())[0]

    img = page_req.find('img', id=f'page{page}')['src']
    print(img)

    if img is None:
        #not sure if this works on all canvas but for now w.e
        manga_title = page_req.select_one('#series').get_text().replace(' ', '-')
        chapter = re.findall('[0-9]+', page_req.select_one('div >  h3 > span:nth-child(3)').get_text())[0]
        img = f'https://iweb7.mangapicgallery.com/imgfiles/{manga_title}/{chapter}/00{page}.png'
        
    browser.close()
    return [img]