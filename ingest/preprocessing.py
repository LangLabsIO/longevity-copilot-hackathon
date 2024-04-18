import os
import requests
import feedparser

from sqlalchemy.orm import Session
from models import Article, engine
from dotenv import load_dotenv
from unstructured.ingest.connector.local import SimpleLocalConfig
from unstructured.ingest.interfaces import PartitionConfig, ProcessorConfig, ReadConfig
from unstructured.ingest.runner import LocalRunner
from unstructured.ingest.connector.vectara import (
    SimpleVectaraConfig,
    VectaraAccessConfig,
    WriteConfig,
)
from unstructured.ingest.runner.writers.vectara import VectaraWriter

from bs4 import BeautifulSoup
import re


# Load environment variables
load_dotenv()

# Unstructured and Vectara API keys
VECTARA_API_KEY = os.getenv("VECTARA_API_KEY")
VECTARA_CUSTOMER_ID = os.getenv("VECTARA_CUSTOMER_ID")
VECTARA_CORPUS_ID = os.getenv("VECTARA_CORPUS_ID")


# Vectara upload URL
VECTARA_ENDPOINT = (
    f"https://api.vectara.io/v1/corpus/{VECTARA_CUSTOMER_ID}/{VECTARA_CORPUS_ID}/ingest"
)

# Example RSS feed URLs (simplified for demonstration)
RSS_FEEDS = {
    "Nature Aging": "https://www.nature.com/nataging.rss",
    "ScienceDaily - Healthy Aging News": "https://www.sciencedaily.com/rss/health_medicine/healthy_aging.xml",
}


def clear_database():
    SessionLocal = Session(bind=engine)
    SessionLocal.query(Article).delete()
    SessionLocal.commit()
    SessionLocal.close()


# Function to fetch and process articles
def fetch_and_process_articles():
    try:
        print("fetch_and_process_articles called")
        SessionLocal = Session(bind=engine)
        for name, url in RSS_FEEDS.items():
            print(f"Processing RSS feed: {url}")
            try:
                articles = fetch_rss_feed(url)
            except Exception as e:
                print(f"Failed to fetch RSS feed from {url}: {e}")
                continue

            for article in articles:
                print(f"Processing article: {article['url']}")
                if not article_exists(SessionLocal, article["url"]):
                    print(
                        f"Article does not exist, preprocessing and ingesting: {article['url']}"
                    )
                    try:
                        # Download the webpage HTML
                        response = requests.get(article["url"])
                        soup = BeautifulSoup(response.text, "html.parser")

                        # Extract the research paper content
                        content = "\n".join([p.get_text() for p in soup.find_all("p")])

                        # Generate the filename from the article title, replacing invalid characters
                        title = article["title"]
                        filename = re.sub(
                            r'[\\/:"*?<>|]', "_", title
                        )  # Replace invalid characters with _

                        # Save the content to a local file
                        dir_path = "local-ingest"
                        os.makedirs(dir_path, exist_ok=True)
                        file_path = f"{dir_path}/{filename}.txt"
                        with open(file_path, "w") as file:
                            file.write(content)

                        # Preprocess the article content
                        print("Preprocessing and ingesting article content")
                        writer = VectaraWriter(
                            connector_config=SimpleVectaraConfig(
                                access_config=VectaraAccessConfig(
                                    oauth_client_id=os.getenv(
                                        "VECTARA_OAUTH_CLIENT_ID"
                                    ),
                                    oauth_secret=os.getenv("VECTARA_OAUTH_SECRET"),
                                ),
                                customer_id=os.getenv("VECTARA_CUSTOMER_ID"),
                                corpus_name="longevity",
                            ),
                            write_config=WriteConfig(),
                        )
                        # Ingest the preprocessed content into Vectara
                        runner = LocalRunner(
                            processor_config=ProcessorConfig(
                                verbose=True,
                                output_dir="local-ingest-output",
                                num_processes=2,
                            ),
                            connector_config=SimpleLocalConfig(
                                input_path=file_path,
                            ),
                            read_config=ReadConfig(),
                            partition_config=PartitionConfig(),
                            writer=writer,
                            writer_kwargs={},
                        )
                        runner.run()

                        # Upload the preprocessed article to Vectara
                        upload_to_vectara(article)
                    except Exception as e:
                        print(f"Failed to preprocess and ingest article content: {e}")
                        continue

                    log_article(SessionLocal, article["title"], article["url"])
        SessionLocal.close()
    except Exception as e:
        print(f"An error occurred in fetch_and_process_articles: {e}")


def article_exists(session: Session, url: str) -> bool:
    return session.query(Article).filter(Article.url == url).first() is not None


def log_article(session: Session, title: str, url: str):
    new_article = Article(title=title, url=url)
    session.add(new_article)
    session.commit()


def upload_to_vectara(article):
    headers = {"Authorization": f"Bearer {VECTARA_API_KEY}"}
    data = {
        "content": article["content"],
        "metadata": {
            "title": article["title"],
            "url": article["url"],
        },
        "external_id": article["url"],
    }
    response = requests.post(VECTARA_ENDPOINT, json=data, headers=headers)
    if response.status_code != 200:
        print(f"Failed to upload to Vectara: {response.text}")


def fetch_rss_feed(url):
    feed = feedparser.parse(url)
    articles = []
    for entry in feed.entries:
        articles.append(
            {
                "title": entry.title,
                "url": entry.link,
                "content": entry.summary,
            }
        )
    return articles
