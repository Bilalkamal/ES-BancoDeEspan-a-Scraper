# constants.py

# Time in seconds between requests
REQUEST_DELAY = 10

# Maximum backoff time in seconds (5 minutes)
MAX_BACKOFF_TIME = 300
# Base URL for Banco de España
BASE_URL = "https://www.bde.es"


# URL mappings for different document types in both languages
URL_MAPPINGS = {
    "Press releases and briefing notes": [
        "/wbe/en/noticias-eventos/actualidad-banco-espana/notas-banco-espana/",
        "/wbe/es/noticias-eventos/actualidad-banco-espana/notas-banco-espana/"
    ],
    "Speeches": [
        "/wbe/en/noticias-eventos/actualidad-banco-espana/intervenciones-publicas/",
        "/wbe/es/noticias-eventos/actualidad-banco-espana/intervenciones-publicas/"
    ],
    "Articles and interviews": [
        "/wbe/en/noticias-eventos/actualidad-banco-espana/articulos-entrevistas-alta-administracion/",
        "/wbe/es/noticias-eventos/actualidad-banco-espana/articulos-entrevistas-alta-administracion/"
    ]
}

# Custom headers for HTTP requests
HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36"
}



