# Banco de España Document Scraper

## Introduction

This project is a robust web scraper tailored for downloading vital documents from the Banco de España website. It's designed to handle a range of documents including speeches, interviews, and press releases in both English and Spanish within specified date ranges.

## Project Structure

```
.
├── README.md
├── app
│   ├── __init__.py
│   ├── constants.py
│   ├── document_parser.py
│   ├── scraper.py
│   └── utils.py
├── data
├── logs
├── main.py
├── requirements.txt
└── tests
    ├── __init__.py
    ├── test_document_parser.py
    └── test_scraper.py
```

```
5 directories, 13 files
```

## Setup and Installation

1. Clone the repository to your local machine.
2. Install the necessary dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the `main.py` script to start the scraping process. The script is set up with predefined date ranges and document types, but these can be adjusted in the script.

Default settings:

- Start Date: November 1, 2022
- End Date: December 31, 2022
- Document Types: Speeches, Press releases, and Interviews

Execute with:

```bash
python main.py
```

## Features

- **Targeted Scraping**: Downloads documents based on date range and type, in English and Spanish.
- **Robustness**: Includes rate limiting, exponential backoff, and mimics browser request headers.
- **Efficiency**: In-memory processing for fast and efficient data handling.
- **Logging**: Comprehensive logging for tracking and debugging.
- **Error Handling**: Gracefully manages request failures and unexpected responses.

## Modules

- `scraper.py`: Core scraping logic for retrieving document URLs and handling data.
- `document_parser.py`: Processes and extracts information from documents.
- `utils.py`: Provides utility functions like logging setup and JSON file writing.
- `constants.py`: Hosts configuration constants such as URL patterns and request headers.

## Testing

Automated tests cover critical components and functionalities. Run tests using:

```bash
pytest
```

## Output

The script outputs a JSON file in the `data` directory with metadata, errors, and success logs.
