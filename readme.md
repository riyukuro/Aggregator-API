# Simple selfhosted manga aggregator API
- Primarily for use with Tachiyomi to avoid sources blocking it / cat and mouse games.
- The developer of this application does not have any affiliation with the content providers available.
- This project is for learning purposes only.

# Source Functions
- `fetch_latest`
    - Fetches latest updated manga
    - Endpoint: /latest
- `fetch_popular`
    - Fetches popular manga
    - Endpoint: /popular
- `fetch_search`
    - Fetches search results
    - Endpoint: /search
- `fetch_manga`
    - Fetches manga details & chapter links/titles
    - Endpoint: /manga
- `fetch_pages`
    - Fetches chapter pages/images
    - Endpoint: /pages 

# Latest/Popular/Search
- {url}/latest?source={source}
- {url}/popular?source={source}
- {url}/search?source={source}&search={search}

## Latest/Popular/Search Structure
```json
{
    "manga_title": "",
    "manga_url": "",
    "manga_cover": ""
}
```

# Manga Details
- {url}/manga?source={source}&slug={manga_slug}

## Manga Details Structure
```json
{
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
        "chapter_slug": ""
        }
    ]
}
```

# Pages
- {url}/pages?source={source}&slug={chapter_slug}
- Returns a list of pages in a chapter