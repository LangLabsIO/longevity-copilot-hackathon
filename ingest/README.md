# Longevity Copilot - Ingest Directory

Welcome to the Ingest Directory of the Longevity Copilot project. This directory contains the scripts for data ingestion and preprocessing. The main components of this directory are `main.py`, `preprocessing.py`, and `models.py`.

## Overview

The ingest project is responsible for fetching, processing, and ingesting articles from various RSS feeds into the Vectara platform. It uses the Unstructured.io library for data handling and processing, and SQLAlchemy for database operations.

### main.py

This is the entry point of the ingest project. It sets up a FastAPI application and a background scheduler that periodically calls the `fetch_and_process_articles` function from `preprocessing.py`. Note that the cron jobs are the primary way this directory should be used, but they are commented out for demonstration purposes.

### preprocessing.py

This script contains the main logic for fetching articles from RSS feeds, preprocessing the article content, and ingesting the preprocessed content into Vectara. It also handles logging of processed articles into a local SQLite database.

### models.py

This script defines the SQLAlchemy model for the `Article` table in the SQLite database.

## Getting Started

To run the ingest project, you need to have Python 3.10+ installed. You also need to install the required Python packages listed in `requirements.txt`.

### Installation

1. Clone the repository and navigate to the ingest directory:
   bash
   git clone https://github.com/your-repo/longevity-copilot-hackathon.git
   cd longevity-copilot-hackathon/ingest

2. Install the required Python packages:
   bash
   pip install -r requirements.txt

### Usage

To start the ingest project, run the `main.py` script:
bash
python main.py

This will start a FastAPI application and a background scheduler that periodically calls the `fetch_and_process_articles` function from `preprocessing.py`.

### Configuration

The ingest project uses environment variables for configuration. You need to create a `.env` file in the `ingest` directory with the following variables:

bash

VECTARA_API_KEY=your_vectara_api_key

VECTARA_CUSTOMER_ID=your_vectara_customer_id

VECTARA_CORPUS_ID=your_vectara_corpus_id

VECTARA_OAUTH_CLIENT_ID=your_vectara_oauth_client_id

VECTARA_OAUTH_SECRET=your_vectara_oauth_secret

Replace `your_vectara_api_key`, `your_vectara_customer_id`, `your_vectara_corpus_id`, `your_vectara_oauth_client_id`, and `your_vectara_oauth_secret` with your actual Vectara API key, customer ID, corpus ID, OAuth client ID, and OAuth secret, respectively.

### Testing

You can test the ingest project by navigating to `http://localhost:8000` in your web browser. You should see a message saying "Automated Research Ingestion Pipeline is Running".
