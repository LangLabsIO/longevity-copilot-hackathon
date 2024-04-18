from fastapi import FastAPI
from apscheduler.schedulers.background import BackgroundScheduler
from preprocessing import fetch_and_process_articles, clear_database

app = FastAPI()

def main():
    # Clear the database
    clear_database()

    # Call the function directly for immediate execution
    fetch_and_process_articles()

    scheduler = BackgroundScheduler()
    # scheduler.add_job(
    #   fetch_and_process_articles, "cron", week="*", day_of_week="sun"
    # )  # Weekly on Sunday
    # scheduler.add_job(fetch_and_process_articles, "interval", minutes=1)
    scheduler.start()

@app.get("/")
async def root():
    return {"message": "Automated Research Ingestion Pipeline is Running"}

if __name__ == '__main__':
    main()
