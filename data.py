from dataclasses import dataclass


@dataclass
class LPR:
    source: str
    manga_title: str
    manga_slug: str
    manga_cover: str

    def format(self):
        return {
            "manga_title": self.manga_title, 
            "manga_url": f"/manga?source={self.source}&slug={self.manga_slug}", 
            "manga_cover": self.manga_cover
            }

@dataclass
class MANGA:
    source: str
    manga_title: str
    manga_cover: str
    manga_desc: str
    manga_status: str
    manga_author: str
    manga_artist: str
    manga_genres: list
    manga_chapters: list

    def format(self):
        return {
        'manga_title': self.manga_title,
        'manga_cover': self.manga_cover,
        'manga_desc': self.manga_desc,
        'manga_status': self.manga_status,
        'manga_author': self.manga_author,
        'manga_artist': self.manga_artist,
        'manga_genres': self.manga_genres,
        'manga_chapters': self.manga_chapters
        }

@dataclass
class CHAPTER:
    source: str
    chapter_title: str
    chapter_slug: str

    def format(self):
        return {
            "chapter_title": self.chapter_title,
            "chapter_url": f'/pages?source={self.source}&slug={self.chapter_slug}'
            }