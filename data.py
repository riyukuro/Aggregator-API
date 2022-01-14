from dataclasses import dataclass


@dataclass
class LPR:
    source: str
    manga_title: str
    manga_slug: str
    manga_cover: str

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