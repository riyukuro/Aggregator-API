from bs4 import BeautifulSoup as bs
import requests as r

header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
manga_url = 'https://www.mangago.me/read-manga/arousing_taste/'

req = bs(r.get(manga_url, headers=header).text, 'html.parser')

#print(req.select_one('tbody:nth-child(1) > tr > td > h4 > a').text)

chapter_url = 'https://www.mangago.me/read-manga/maid_in_heaven_1/uu/br_chapter-64774/pg-1'
req2 = bs(r.get(chapter_url, headers=header).text, 'html.parser')

#print(req2.find_all('#dropdown-menu-page > li'))
print(req2)