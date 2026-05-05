# Youtube End-to-End Data Engineering Pipeline (Youtube_E2E_DE)

This project is an End-to-End Data Engineering pipeline that extracts data from YouTube channels using the YouTube Data API v3, processes it, and loads it into a PostgreSQL Data Warehouse. The pipeline is orchestrated using Apache Airflow and fully containerized with Docker.

## Project Overview

The data pipeline consists of two main workflows (DAGs):

1. **`produce_json`**: Connects to the YouTube Data API to fetch a channel's uploaded videos, paginates through the results, extracts detailed statistics (views, likes, comments, duration), and saves the raw data as a JSON file partitioned by date.
2. **`update_db`**: Reads the generated JSON file and performs an ETL/ELT process to load the data into a PostgreSQL database. It populates both `staging` and `core` schemas, handling data transformations and modifications.

## Tech Stack & Architecture

- **Data Extraction**: Python, YouTube Data API v3
- **Orchestration**: Apache Airflow (CeleryExecutor)
- **Database / Data Warehouse**: PostgreSQL
- **Containerization**: Docker & Docker Compose
- **Caching / Broker**: Redis
- **Database GUI**: DBeaver (used for visualizing and querying PostgreSQL data)

## Project Structure

- `dags/`: Contains the Airflow DAG definitions (`main.py`) and task modules.
  - `api/`: Scripts for YouTube API interaction (`video_stats.py`).
  - `datawarehouse/`: Scripts for data loading, transformation, and modification (`dwh.py`, `data_utils.py`, `data_modification.py`, etc.).
- `docker-compose.yaml`: Configuration for spinning up Airflow, Postgres, and Redis containers.
- `requirements.txt`: Python dependencies.
- `.env`: Environment variables (API keys, database credentials).

## Installation and Setup

### Prerequisites

- Docker and Docker Compose installed
- DBeaver (optional, for viewing the database)
- YouTube Data API Key

### Running with Docker

1. Clone the repository and navigate to the project directory.
2. Ensure your `.env` file is configured with the necessary API keys and database credentials:
   ```env
   API_KEY=your_youtube_api_key
   CHANNEL_HANDLE=your_target_channel_handle
   # ... plus Postgres/Airflow environment variables
   ```
3. Initialize Airflow:
   ```bash
   docker-compose up airflow-init
   ```
4. Start the services:
   ```bash
   docker-compose up -d
   ```
5. Access the Airflow Web UI at `http://localhost:8080` to trigger and monitor the DAGs.

### Viewing Data with DBeaver

You can use DBeaver to connect to the PostgreSQL instance running in Docker and view the data intuitively through a GUI.

1. Open DBeaver and create a new PostgreSQL connection.
2. Set the Host to `localhost` and the Port to `5432` (or the port defined in your `.env` / `docker-compose.yaml`).
3. Enter the database name, username, and password as specified in your configuration (e.g., `ELT_DATABASE_NAME`, `ELT_DATABASE_USERNAME`).
4. Once connected, you can browse the `staging` and `core` schemas to verify the data ingestion and transformation.

## Project Timeline & Recent Updates

- **Airflow Orchestration & Dockerization**: Migrated the pipeline to run on Apache Airflow with CeleryExecutor and Postgres backend, fully containerized using Docker.
- **Data Warehouse Operations**: Added `staging_table` and `core_table` processing to move raw JSON data into structured Postgres tables.
- **Script Formatting and Documentation**: Added comprehensive docstrings to all functions in `video_stats.py`, `data_utils.py`, and `data_modification.py`. Cleaned up code formatting.
- **Initial Development**: Built the YouTube Data API extraction logic, handling pagination and saving detailed metadata to JSON files.
