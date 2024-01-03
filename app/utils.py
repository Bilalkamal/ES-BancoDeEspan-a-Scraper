# utils.py

import logging 
import os
import json
from datetime import datetime


def setup_logging():
    """
    Sets up logging for the application.

    This function creates a log directory if it doesn't exist and sets up a log file with the current date as the filename.
    The log file will contain log messages with the format: "<timestamp> <log_level>: <message>".

    Args:
        None

    Returns:
        None
    """
    log_directory = os.path.join(os.path.dirname(__file__), '..', 'logs')
    os.makedirs(log_directory, exist_ok=True)
    log_filename = os.path.join(log_directory, datetime.now().strftime("%Y-%m-%d-run.log"))
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(levelname)s: %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        filename=log_filename,
                        filemode='w')


def write_json_to_disk(json_object, query_details):
    """
    Writes a JSON object to disk.

    Args:
        json_object (dict): The JSON object to be written.
        query_details (dict): Details of the query used to generate the JSON object.

    Returns:
        None
    """
    data_directory = os.path.join(os.path.dirname(__file__), '..', 'data')
    os.makedirs(data_directory, exist_ok=True)
    filename = f"{query_details['start_date']}_{query_details['end_date']}_{query_details['run_date']}.json"
    file_path = os.path.join(data_directory, filename)
    with open(file_path, 'w') as f:
        json.dump(json_object, f)
    logging.info(f"Successfully wrote JSON to disk: {filename}")