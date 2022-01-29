def formatting(data: int, source: str, *argv):
    """0 = LPS, 1 = Manga, 2 = Chapter, 3 = Paged"""
    if data is 0: # LPS
        """
        arg1 = title: str
        arg2 = slug : str
        arg3 = manga_cover : str
        """
        return {
            "manga_title": argv[0],
            "manga_url": "/manga?source=%s&slug=%s" % (source, argv[1]), 
            "manga_cover": argv[2]
        }
    if data is 1: # Manga
        """
        args1 = manga_title: str
        args2 = manga_cover: str
        args3 = manga_desc: str
        args4 = manga_status: str
        args5 = manga_author: str
        args6 = manga_artist: str
        args7 = manga_genres: list
        args8 = manga_chapters: list
        """
        return {
            'manga_title': argv[0],
            'manga_cover': argv[1],
            'manga_desc': argv[2],
            'manga_status': argv[3],
            'manga_author': argv[4],
            'manga_artist': argv[5],
            'manga_genres': argv[6],
            'manga_chapters': argv[7]
        }
    if data is 2: #chapter
        """
        args1 = chapter_title
        args2 = chapter_slug
        """
        return {
            "chapter_title": argv[0],
            "chapter_url": '/pages?source=%s&slug=%s' % (source, argv[1])
            }
    if data is 3: # paged
        #args1 = page_slug: str

        return '/page?source=%s&slug=%s' % (source, argv[0])