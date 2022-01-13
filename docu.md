# Latest/Popular/Search
- {url}/latest?{source}
- {url}/popular?{source}
- {url}/search?{source}&{search}

## Latest/Popular/Search Structure
```json
{"source": {
    "manga_title": "",
    "manga_url": "",
    "manga_cover": ""
    }
}
```

# Manga Details
- {url}/manga?{source}&slug={manga_slug}

## Manga Details Structure
```json
{"source": {
    "manga_title": "",
    "manga_cover": "",
    "manga_desc": "",
    "manga_status": "",
    "manga_author": "",
    "manga_artist": "",
    "manga_genres": [],
    "manga_chapters": [
        {
        "chapter_title": "",
        "chapter_url": ""
            }
        ]
    }
}
```

# Pages
- {url}/pages?source={source}&slug={chapter_slug}
- Returns a list of pages in a chapter