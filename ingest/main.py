from fastapi import FastAPI
from apscheduler.schedulers.background import BackgroundScheduler

app = FastAPI()


def fetch_and_process_articles():
    # This function will fetch new articles, preprocess them, and upload to Vectara

    # Fetch articles

    print("Fetching articles")

    # Preprocess articles
    print("Preprocessing articles")

    # Upload to Vectara
    print("Uploading to Vectara")
    pass


scheduler = BackgroundScheduler()
scheduler.add_job(
    fetch_and_process_articles, "cron", week="*", day_of_week="sun"
)  # Weekly on Sunday
scheduler.start()


@app.get("/")
async def root():
    return {"message": "Automated Research Ingestion Pipeline is Running"}
