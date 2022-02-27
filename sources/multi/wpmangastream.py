import re
from server import driver
from bs4 import BeautifulSoup as bs
from data import formatting

class WPMangaStream:
    source_name: str = None
    isPaged: bool = False
    base_url: str = None
    popular_url: str = '{0}/manga/?page=1&order=popular'
    latest_url: str = '{0}/manga/?page=1&order=update'
    search_url: str = '{0}/?s={1}'
    popular_selector: str = 'bsx'
    latest_selector: str = popular_selector
    search_selector: str = popular_selector

    title_selector: str = None
    cover_selector: str = None
    desc_selector: str = None
    status_selector: str = None
    page_selector: str = 'div#readerarea'
    
    
    browser = driver()


    def fetch_lps(self, *args):
        entries = []
        req = bs(self.browser.get(args[0]).text, 'html.parser')
        for i in req.find_all('div', args[1]):
            entries.append(formatting(
                0,
                source = self.source_name,
                title = i.a['title'],
                slug = '/'+i.a['href'].strip(self.base_url),
                cover = i.img['src']
            ))
        return entries

    def fetch_latest(self): return self.fetch_lps(self.latest_url.format(self.base_url), self.latest_selector)

    def fetch_popular(self): return self.fetch_lps(self.popular_url.format(self.base_url), self.popular_selector)

    def fetch_search(self, term): return self.fetch_lps(self.search_url.format(self.base_url, term), self.search_selector)
    
    def fetch_manga(self, slug): 
        req = bs(self.browser.get(self.base_url+slug).text, 'html.parser')

        genres = []    
        chapters = []

        if chapter_list := req.find('div', id='chapterlist'):
            for i in chapter_list.find_all('li'):
                chapters.append(formatting(
                    2,
                    source = self.source_name,
                    title = i.div.div.a.find('span', class_='chapternum').get_text().strip(),
                    slug = i.a['href'].replace(self.base_url, '')
                ))
        else: 
            for i in req.select('.bixbox li'):
                chapters.append(formatting(
                    2,
                    source = self.source_name,
                    title = i.find('a').get_text().strip(),
                    slug = i.find('a')['href'].split('/')[-1].strip(self.base_url)
                ))

        cover_r = req.select_one(self.cover_selector)
        
        if cover_r['src'] is not None: cover = cover_r['src']
        else: cover = cover_r['data-src']
        status_check = req.select_one(self.status_selector).get_text().strip()

        if any(re.findall(r'ongoing|devam ediyor', status_check, re.IGNORECASE)):
            status = 'ongoing'
        elif any(re.findall(r'completed|tamamlandı', status_check, re.IGNORECASE)):
            status = 'complete'
        elif any(re.findall(r'hiatus|bırakıldı', status_check, re.IGNORECASE)):
            status = 'hiatus'
        elif any(re.findall(r'dropped|durduruldu', status_check, re.IGNORECASE)):
            status = 'suspended'
        else: status = None

        return formatting(
            1,
            source = self.source_name,
            title = req.select_one(self.title_selector).get_text().strip(),
            cover = cover,
            desc = req.select_one(self.desc_selector).get_text().strip(),
            status = status,
            author = '',
            artist = '',
            genres = genres,
            chapters = chapters
        )
        
    def fetch_pages(self, slug):
        req = bs(self.browser.get(self.base_url+slug).text, 'html.parser')

        if page_elements := req.select_one(self.page_selector):
            if page_elements.img['src']: 
                page_list = [i['src'] for i in page_elements.find_all('img')]
            else: page_list = [i['data-src'] for i in page_elements.find_all('img')]

            #if script_pages := any(re.findall(r'\\\"images.*?:.*?(\\[.*?\\])', re.IGNORECASE)):
            #    print(script_pages)
                
        return page_list

    def fetch_page(self):
        return None