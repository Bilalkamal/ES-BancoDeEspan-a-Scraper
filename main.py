# main.py
from datetime import date, datetime
from app.scraper import BancoDeEspanaScraper
from app.utils import setup_logging, write_json_to_disk


def main():
    setup_logging()

    start_date = date.fromisoformat('2022-11-01')
    end_date = date.fromisoformat('2022-12-31')
    # Options: "Speeches", "Press releases and briefing notes", "Articles and interviews"
    document_types = ["Speeches", "Press releases and briefing notes", "Articles and interviews"]

    scraper = BancoDeEspanaScraper(start_date, end_date, document_types)
    results = scraper.scrape_documents()
    output = {
        "metadata": {
            "query_start_date": start_date.strftime("%Y-%m-%d"),
            "query_end_date": end_date.strftime("%Y-%m-%d"),
            "run_start_datetime": datetime.now().isoformat(),
            "schema": "v2"
        },
        "errors": results["errors"],
        "successes": results["successes"]
    }

    query_details = {
        "start_date": start_date.strftime("%Y-%m-%d"),
        "end_date": end_date.strftime("%Y-%m-%d"),
        "run_date": date.today().strftime("%Y-%m-%d")
    }
    write_json_to_disk(output, query_details)

if __name__ == "__main__":
    main()