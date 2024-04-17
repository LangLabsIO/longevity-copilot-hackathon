import os
import requests
from sqlalchemy.orm import Session
from models import Article, engine
from dotenv import load_dotenv
from unstructured import UnstructuredClient  # Add this line


# Load environment variables
load_dotenv()

# Unstructured and Vectara API keys
UNSTRUCTURED_API_KEY = os.getenv("UNSTRUCTURED_API_KEY")
VECTARA_API_KEY = os.getenv("VECTARA_API_KEY")
VECTARA_CUSTOMER_ID = os.getenv("VECTARA_CUSTOMER_ID")
VECTARA_CORPUS_ID = os.getenv("VECTARA_CORPUS_ID")

# Initialize Unstructured.io client
unstructured_client = UnstructuredClient(api_key=UNSTRUCTURED_API_KEY)

# Vectara upload URL
VECTARA_ENDPOINT = (
    f"https://api.vectara.io/v1/corpus/{VECTARA_CUSTOMER_ID}/{VECTARA_CORPUS_ID}/ingest"
)

# Example RSS feed URLs (simplified for demonstration)
RSS_FEEDS = {
    "Nature Aging": "Nature Aging RSS Feed URL",
    "ScienceDaily - Healthy Aging News": "ScienceDaily Healthy Aging News RSS",
    # Add other RSS feeds as needed
}


# Function to fetch and process articles
def fetch_and_process_articles():
    SessionLocal = Session(bind=engine)
    for name, url in RSS_FEEDS.items():
        try:
            articles = fetch_rss_feed(
                url
            )  # Implement this function based on the RSS package or custom parsing logic
        except Exception as e:
            print(f"Failed to fetch RSS feed from {url}: {e}")
            continue

        for article in articles:
            if not article_exists(SessionLocal, article["url"]):
                try:
                    processed_content = unstructured_client.preprocess(
                        article["content"]
                    )
                except Exception as e:
                    print(f"Failed to preprocess article content: {e}")
                    continue

                upload_to_vectara(processed_content)
                log_article(SessionLocal, article["title"], article["url"])
    SessionLocal.close()


def article_exists(session: Session, url: str) -> bool:
    return session.query(Article).filter(Article.url == url).first() is not None


def log_article(session: Session, title: str, url: str):
    new_article = Article(title=title, url=url)
    session.add(new_article)
    session.commit()


def upload_to_vectara(content: str):
    headers = {"Authorization": f"Bearer {VECTARA_API_KEY}"}
    data = {
        # Structure the data as required by Vectara's API
        "content": content,
        # Add other necessary fields
    }
    response = requests.post(VECTARA_ENDPOINT, json=data, headers=headers)
    if response.status_code != 200:
        print(f"Failed to upload to Vectara: {response.text}")


# Placeholder for the RSS feed fetching function
def fetch_rss_feed(url):
    # Use requests or an RSS feed parser library to fetch and parse the feed
    # Return a list of articles with 'title', 'url', and 'content' keys
    return []
