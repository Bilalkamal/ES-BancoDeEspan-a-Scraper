# scraper.py
from bs4 import BeautifulSoup
from datetime import datetime
import logging
import requests
from .constants import BASE_URL, URL_MAPPINGS, HEADERS
from .document_parser import DocumentParser

class BancoDeEspanaScraper:
    """
    A class for scraping data from the Banco de España website.
    """

    def __init__(self, start_date, end_date, document_types):
        """
        Initialize the BancoDeEspanaScraper object.

        Args:
            start_date (datetime): The start date for the data query.
            end_date (datetime): The end date for the data query.
            document_types (list): A list of document types to scrape.
        """
        self.start_date = start_date
        self.end_date = end_date
        self.document_types = document_types
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
        self.parser = DocumentParser(self.session)

    def scrape_documents(self):
        """
        Scrape documents from the Banco de España website.

        Returns:
            dict: A dictionary containing scraped document details and errors.
        """
        results = {"errors": [], "successes": []}

        urls = self.scrape_search_results()
        logging.info(f"Total URLs collected: {len(urls)}")

        for doc_type, url in urls:
            try:
                logging.info(f"Scraping URL: {url} of type {doc_type}")
                response = self.session.get(url)
                response.raise_for_status()

                html_content = response.text
                parsed_result = self.parser.parse_document(html_content, url, doc_type)
                if not parsed_result:
                    results["errors"].append({
                        "datetime_accessed": datetime.now().isoformat(),
                        "document_url": url,
                        "processing_error": "No parsed result returned"
                    })
                    continue
                results["successes"].append(parsed_result)
                logging.info(f"Successfully scraped URL: {url}")

            except requests.RequestException as e:
                logging.error(f"An error occurred: {e}")
                results["errors"].append({
                    "datetime_accessed": datetime.now().isoformat(),
                    "document_url": url,
                    "processing_error": str(e)
                })
        return results

    def scrape_search_results(self):
        """
        Scrape search results for specified document types and date range.

        Returns:
            list: List of tuples containing document type and URL to scrape.
        """
        urls_to_collect = []
        for doc_type in self.document_types:
            logging.info(f"Scraping document type: {doc_type}")
            for url in URL_MAPPINGS.get(doc_type, []):
                page = 1
                while True:
                    logging.info(f"Scraping page {page} of search results for {doc_type}...")
                    try:
                        formatted_start_date = self.start_date.strftime("%m%Y")
                        formatted_end_date = self.end_date.strftime("%m%Y")
                        full_url = f"{BASE_URL}{url}?page={page}&start={formatted_start_date}&end={formatted_end_date}&sort=DESC"
                        response = self.session.get(full_url)
                        response.raise_for_status()
                        soup = BeautifulSoup(response.text, 'html.parser')
                        links = self.find_links_in_page(soup)
                        
                        if not links:
                            break

                        urls_to_collect.extend([(doc_type, BASE_URL + link['href']) for link in links if 'href' in link.attrs])
                        page += 1
                    except requests.RequestException as e:
                        logging.error(f"An error occurred: {e}")
                        break
        return urls_to_collect

    def find_links_in_page(self, soup):
        """
        Find links to documents in a search result page.

        Args:
            soup: BeautifulSoup object representing the search result page.

        Returns:
            list: List of BeautifulSoup elements representing document links.
        """
        links = soup.select('div.block-search-result__title a')
        alternate_links = soup.select('p.block-search-result__title a')
        links.extend(alternate_links)
        return links
