from sources.multi.wpmangastream import WPMangaStream
#from sources.multi.madara import madara

class asurascans(WPMangaStream):
    source_name = 'asurascans'
    base_url = 'https://www.asurascans.com'

    title_selector = '.entry-title'
    cover_selector = '.thumb img'
    authors_selector = '.infox .fmed:contains("Artist") span, .infox .fmed:contains("Author") span'
    genres_selector = '.infox .mgen a'
    scanlators_selector = '.infox .fmed:contains("Serialization") span'
    status_selector = '.tsinfo .imptdt i'
    desc_selector = '[itemprop="description"]'
