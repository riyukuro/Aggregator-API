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
- `fetch_page`
    - Fetches images for paged sources and returns them as base64.
    - Endpoint: /page

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
        "chapter_url": ""
        }
    ]
}
```

# Pages
- {url}/pages?source={source}&slug={chapter_slug}
- Returns a list of pages in a chapter.
    - If the source isnt paged it returns image urls (otherwise sends a list of /page urls).

# Page
- {url}/page?source={source}&slug={page_slug}
- Returns a single base64 encoded image.
- Used for paged sources.

## Page Structure
```json
{
    "b64": "B64 encoded image"
}