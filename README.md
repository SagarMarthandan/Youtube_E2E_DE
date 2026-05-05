# Youtube_E2E_DE

This project is a data pipeline that extracts data from YouTube channels and saves it to a JSON file.

## Installation

```bash
python3 -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
```

## Project Timeline

- **2026-05-05: Script Formatting and Documentation**
  - Added comprehensive docstrings to all functions in `video_stats.py`.
  - Cleaned up code formatting by removing excessive whitespace and newlines for better readability.
  - Prepared and preserved boilerplate code for upcoming Apache Airflow integration (e.g., `@task` decorators and Airflow variables).

- **Initial Development: YouTube Data Extraction Setup**
  - Created the foundational `video_stats.py` script to interact with the YouTube Data API v3.
  - Implemented functionality to fetch a channel's 'uploads' playlist using a target channel handle.
  - Handled API pagination to retrieve all video IDs within the playlist.
  - Built a batching mechanism to extract detailed statistics (views, likes, comments, duration) and metadata for all collected videos.
  - Set up JSON export to save the extracted data partitioned by the current date (`YT_data_YYYY-MM-DD.json`).
  - Configured environment variables (`.env`) for secure API key and channel handle management.
