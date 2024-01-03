# test_document_parser.py

from app.document_parser import DocumentParser
import pytest
from unittest.mock import MagicMock, Mock
from io import BytesIO
from bs4 import BeautifulSoup
import requests

# Constants for tests
SAMPLE_HTML = "<html><body><h1>Test Title</h1><a href='/test.pdf'>Download PDF</a><div class='block-topics__date'>2022-01-01</div></body></html>"
SAMPLE_PDF_LINK = "/test.pdf"
SAMPLE_DOC_TYPE = "report"
SAMPLE_PDF_CONTENT = b'%PDF-1.4...endobj'  
# Mock session setup
mock_session = MagicMock()
mock_response = MagicMock(spec=requests.Response, content=SAMPLE_PDF_CONTENT)
mock_session.get.return_value = mock_response

@pytest.fixture
def document_parser():
    return DocumentParser(mock_session)

@pytest.fixture
def soup():
    return BeautifulSoup(SAMPLE_HTML, 'html.parser')

def test_find_pdf_links(soup, document_parser):
    links = document_parser.find_pdf_links(soup)
    assert SAMPLE_PDF_LINK in links[0]

def test_extract_document_date(soup, document_parser):
    date = document_parser.extract_document_date(soup)
    assert date == "2022-01-01"

def test_extract_document_title(soup, document_parser):
    title = document_parser.extract_document_title(soup)
    assert title == "Test Title"


def test_get_pdf_data_encoded(document_parser):
    pdf_content = BytesIO(SAMPLE_PDF_CONTENT)
    encoded_data = document_parser.get_pdf_data_encoded(pdf_content)
    assert isinstance(encoded_data, str)


def test_extract_text_from_text_pdf(document_parser):
    pdf_content = BytesIO(SAMPLE_PDF_CONTENT)
    text = document_parser.extract_text_from_text_pdf(pdf_content)
    assert isinstance(text, str)

def test_extract_text_from_image_pdf(document_parser):
    pdf_content = BytesIO(SAMPLE_PDF_CONTENT)
    text = document_parser.extract_text_from_image_pdf(pdf_content)
    assert isinstance(text, str)


