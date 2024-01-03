# document_parser.py

import base64
import zlib
import pdfplumber
from pytesseract import image_to_string
from pdf2image import convert_from_bytes
from langdetect import detect
from bs4 import BeautifulSoup
from datetime import datetime
import logging
from io import BytesIO
import tabula
from .constants import HEADERS, BASE_URL

class DocumentParser:
    """
    A class for parsing documents obtained from the Bundesbank website.
    """

    def __init__(self, session):
        """
        Initialize the DocumentParser object.

        Args:
            session: The HTTP session used for making requests.
        """
        self.session = session

    def parse_document(self, html_content, url, doc_type):
        """
        Parse a document obtained from the Bundesbank website.

        Args:
            html_content (str): The HTML content of the document.
            url (str): The URL of the document.
            doc_type (str): The type of the document.

        Returns:
            dict: A dictionary containing parsed document details.
        """
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')

        # Extract document date and title
        document_date = self.extract_document_date(soup)
        document_title = self.extract_document_title(soup)

        # Find PDF links in the HTML content
        pdf_links = self.find_pdf_links(soup)

        document_pdf_encoded, document_text, document_tables, language = "", "", [], ""
        
        if pdf_links:
            try:
                # Download the first PDF linked in the HTML content
                pdf_response = self.session.get(pdf_links[0], stream=True, headers=HEADERS, timeout=20)
                pdf_response.raise_for_status()
                pdf_content = BytesIO(pdf_response.content)

                # Encode and extract text from the PDF
                document_pdf_encoded = self.get_pdf_data_encoded(pdf_content)
                document_text, language = self.extract_text_from_pdf(pdf_content)
                
            except Exception as e:
                logging.error(f"Error downloading or processing PDF {document_title}: {e}")
                return None
            
            # Extract tables from the PDF
            document_tables = self.extract_tables_from_pdf(pdf_content)
            if not document_tables:
                document_tables = []

        return {
            "datetime_accessed": datetime.now().isoformat(),
            "language": language,
            "document_type": doc_type,
            "document_author": "",  
            "document_date": document_date,
            "document_title": document_title,
            "document_text": document_text,
            "document_html": html_content if not pdf_links else "",
            "document_url": url,
            "document_pdf_encoded": document_pdf_encoded,
            "document_tables": document_tables
        }

    def find_pdf_links(self, soup):
        """
        Find PDF links in the HTML content.

        Args:
            soup: BeautifulSoup object representing the HTML content.

        Returns:
            list: List of PDF links found in the HTML content.
        """
        links = soup.find_all('a', href=True)
        return [BASE_URL + link['href'] for link in links if link['href'].endswith('.pdf') and not link['href'].startswith('http')]

    def extract_document_date(self, soup):
        """
        Extract the document date from the HTML content.

        Args:
            soup: BeautifulSoup object representing the HTML content.

        Returns:
            str: The extracted document date.
        """
        date_element = soup.find(class_="block-topics__date")
        return date_element.text.strip() if date_element else ""

    def extract_document_title(self, soup):
        """
        Extract the document title from the HTML content.

        Args:
            soup: BeautifulSoup object representing the HTML content.

        Returns:
            str: The extracted document title.
        """
        title_element = soup.find('h1')
        return title_element.text.strip() if title_element else ""

    def get_pdf_data_encoded(self, pdf_content):
        """
        Encode PDF content using base64 and zlib.

        Args:
            pdf_content: BytesIO object containing PDF content.

        Returns:
            str: Base64 encoded and zlib compressed PDF content.
        """
        return base64.b64encode(zlib.compress(pdf_content.read())).decode()

    def extract_text_from_pdf(self, pdf_content):
        """
        Extract text from the PDF content.

        Args:
            pdf_content: BytesIO object containing PDF content.

        Returns:
            tuple: A tuple containing extracted text and detected language.
        """
        if self.is_scanned_or_image_pdf(pdf_content):
            text = self.extract_text_from_image_pdf(pdf_content)
        else:
            text = self.extract_text_from_text_pdf(pdf_content)
        language = detect(text)
        return text, language

    def is_scanned_or_image_pdf(self, pdf_content):
        """
        Determine if the PDF is scanned or image-based.

        Args:
            pdf_content: BytesIO object containing PDF content.

        Returns:
            bool: True if the PDF is scanned or image-based, False otherwise.
        """
        try:
            with pdfplumber.open(pdf_content) as pdf:
                text = ''.join(page.extract_text() for page in pdf.pages if page.extract_text())
            return not text or len(text.strip()) < 50
        except Exception as e:
            logging.error(f"Error in determining if PDF is scanned/image-based: {e}")
            return True

    def extract_text_from_text_pdf(self, pdf_content):
        """
        Extract text from a text-based PDF.

        Args:
            pdf_content: BytesIO object containing PDF content.

        Returns:
            str: Extracted text from the PDF.
        """
        try:
            with pdfplumber.open(pdf_content) as pdf:
                text = ''.join(page.extract_text() for page in pdf.pages if page.extract_text())
            return text
        except Exception as e:
            logging.error(f"Error extracting text from text-based PDF: {e}")
            return ""

    def extract_text_from_image_pdf(self, pdf_content):
        """
        Extract text from an image-based PDF.

        Args:
            pdf_content: BytesIO object containing PDF content.

        Returns:
            str: Extracted text from the PDF.
        """
        try:
            images = convert_from_bytes(pdf_content.read())
            text = ' '.join(image_to_string(image) for image in images)
            return text
        except Exception as e:
            logging.error(f"Error extracting text from image PDF: {e}")
            return ""

    def extract_tables_from_pdf(self, pdf_content):
        """
        Extract tables from the PDF content.

        Args:
            pdf_content: BytesIO object containing PDF content.

        Returns:
            list: List of extracted tables in tab-separated format.
        """
        try:
            tables = []
            df_list = tabula.read_pdf(pdf_content, pages='all', multiple_tables=True)
            for df in df_list:
                tables.append(df.to_csv(sep='\t', index=False))
            return tables
        except Exception as e:
            logging.error(f"Error extracting tables from PDF: {e}")
            return None
