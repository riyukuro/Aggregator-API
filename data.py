def formatting(type: int, **kwargs):
    """type: 0 = LPS, 1 = Manga, 2 = Chapter, 3 = Paged"""

    match type:
        case 0:
            return {
                "manga_title": kwargs['title'],
                "manga_url": "/manga?source=%s&slug=%s" % (kwargs['source'], kwargs['slug']),
                "manga_cover": kwargs['cover']
            }

        case 1:
            return {
                'manga_title': kwargs['title'],
                'manga_cover': kwargs['cover'],
                'manga_desc': kwargs['desc'],
                'manga_status': kwargs['status'],
                'manga_author': kwargs['author'],
                'manga_artist': kwargs['artist'],
                'manga_genres': kwargs['genres'],
                'manga_chapters': kwargs['chapters']
            }

        case 2:
            return {
                "chapter_title": kwargs['title'],
                "chapter_url": '/pages?source=%s&slug=%s' % (kwargs['source'], kwargs['slug'])
                }

        case 3:
            return '/page?source=%s&slug=%s.png' % (kwargs['source'], kwargs['slug'])

    return 'Invalid Selection'
