from server import driver
from bs4 import BeautifulSoup as bs
from data import formatting
import re

source_name = 'mangago'
isPaged = True

base_url = 'https://www.mangago.me'
latest_url = f'{base_url}/genre/all/1/?f=1&o=1&sortby=update_date&e='
popular_url = f'{base_url}/genre/all/1/?f=1&o=1&sortby=view&e='

browser = driver()

def fetch_latest():
    latest_data = list()
    req = bs(browser.get(latest_url).text, 'html.parser')
    for i in req.select('div.flex1'):
        data = formatting(
            0,
            source_name,
            i.span.get_text(),
            '/' + i.a['href'].lstrip(base_url),
            i.img['data-src']
        )

        latest_data.append(data)

    return latest_data


def fetch_popular():
    popular_data = list()
    req = bs(browser.get(popular_url).text, 'html.parser')
    for i in req.select('div.flex1'):
        data = formatting(
            0,
            source_name,
            i.span.get_text(),
            '/' + i.a['href'].lstrip(base_url),
            i.img['data-src']
        )

        popular_data.append(data)

    return popular_data


def fetch_search(search):
    req = bs(browser.get(f'{base_url}/r/l_search/?name={search}').text, 'html.parser')
    search_data = list()
    for i in req.select_one('#search_list').find_all('li'):
        data = formatting(
            0,
            source_name,
            i.a['title'],
            '/' + i.a['href'].lstrip(base_url),
            i.a.img['src']
        )
        
        search_data.append(data)

    return search_data


def fetch_manga(manga_slug):
    manga_url = base_url + manga_slug
    req = bs(browser.get(manga_url).text, 'html.parser')
    print(browser.get(manga_url).text)

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
        chapter = formatting(
            2,
            source_name,
            " ".join(i.select_one('a').get_text().strip().split()),
            '/' + i.a['href'].lstrip(base_url),
        )
        chapters.append(chapter)

    data = formatting(
        1,
        source_name,
        title,
        cover,
        desc,
        status,
        author,
        artist,
        genres,
        chapters
    )

    return data


def fetch_pages(chapter_slug):
    page_urls = list()

    req = bs(browser.get(f'{base_url}{chapter_slug}', js=True).page_source, 'html.parser')
    for i in req.select_one('#dropdown-menu-page').find_all('li'):
        page_urls.append(formatting(3, source_name, i.a['href']))

    browser.close()
    return {"isPaged": isPaged, "pages": page_urls}


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
    