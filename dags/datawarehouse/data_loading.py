import json
from datetime import date
import logging

logger = logging.getLogger(__name__)


def load_data():
    """Loads YouTube video data from a JSON file named with the current date."""

    # Construct the file path using today's date to match the extraction output
    file_path = f"./data/YT_data_{date.today()}.json"

    try:
        logger.info(f"Processing file: YT_data_{date.today()}")

        # Open and parse the JSON file containing raw video statistics
        with open(file_path, "r", encoding="utf-8") as raw_data:
            data = json.load(raw_data)
        
        return data
    except FileNotFoundError:
        logger.error(f"File not found:{file_path}")
        raise
    except json.JSONDecodeError:
        logger.error(f"Invalid JSON in file: {file_path}")
        raise