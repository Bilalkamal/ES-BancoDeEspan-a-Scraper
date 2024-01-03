import pytest
from unittest.mock import MagicMock, Mock
from io import BytesIO
from bs4 import BeautifulSoup
import requests
from datetime import datetime
from app.scraper import BancoDeEspanaScraper

# Constants for tests
START_DATE = datetime(2022, 1, 1)
END_DATE = datetime(2022, 12, 31)
DOCUMENT_TYPES = ["type1", "type2"]
SAMPLE_HTML = "<html><body><a href='/test.pdf'>Download PDF</a></body></html>"
SAMPLE_DOC_TYPE = "type1"
SAMPLE_PDF_CONTENT = b'%PDF-1.4...endobj'

# Mock session setup
mock_session = MagicMock()
mock_response = MagicMock(spec=requests.Response, content=BytesIO(SAMPLE_PDF_CONTENT).read())
mock_session.get.return_value = mock_response

@pytest.fixture
def scraper():
    return BancoDeEspanaScraper(START_DATE, END_DATE, DOCUMENT_TYPES)


def test_find_links_in_page(scraper):
    html_content = "<div class='block-search-result__title'><a href='/doc1.pdf'>Document 1</a></div>"
    soup = BeautifulSoup(html_content, 'html.parser')

    links = scraper.find_links_in_page(soup)

    assert len(links) == 1
    assert links[0].get('href') == '/doc1.pdf'

def test_find_links_in_page_multiple(scraper):
    html_content = """
    <div class='block-search-result__title'>
        <a href='/doc1.pdf'>Document 1</a>
        <a href='/doc2.pdf'>Document 2</a>
    </div>
    """
    soup = BeautifulSoup(html_content, 'html.parser')

    links = scraper.find_links_in_page(soup)

    assert len(links) == 2
    assert links[0].get('href') == '/doc1.pdf'
    assert links[1].get('href') == '/doc2.pdf'

def test_find_links_in_page_no_links(scraper):
    html_content = "<div class='other-div'><a href='/doc4.pdf'>Document 4</a></div>"
    soup = BeautifulSoup(html_content, 'html.parser')

    links = scraper.find_links_in_page(soup)

    assert len(links) == 0
