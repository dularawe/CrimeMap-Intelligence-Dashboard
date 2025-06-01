from fastapi import FastAPI, HTTPException
from ml_server.rss_scraper import fetch_rss_news
from ml_server.twitter_scraper import fetch_tweets
import logging

app = FastAPI()


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@app.get("/get-latest-crimes")
def get_latest_crimes():
    logging.info("🔍 Starting /get-latest-crimes endpoint")

    rss_data = []
    twitter_data = []

    # Fetch RSS News
    try:
        logging.info("Fetching RSS news...")
        rss_data = fetch_rss_news()
        logging.info(f" RSS fetched: {len(rss_data)} items")
    except Exception as e:
        logging.error(f" Error fetching RSS news: {e}")

    # Fetch Tweets
    try:
        logging.info("Fetching Twitter data...")
        twitter_data = fetch_tweets()
        logging.info(f"Twitter fetched: {len(twitter_data)} items")
    except Exception as e:
        logging.error(f"Error fetching Tweets: {e}")

    # If both sources fail
    if not rss_data and not twitter_data:
        logging.warning("⚠️ No data from either source")
        raise HTTPException(status_code=503, detail="Failed to fetch data from both RSS and Twitter")

    combined_data = rss_data + twitter_data

    return {
        "status": "success",
        "rss_count": len(rss_data),
        "twitter_count": len(twitter_data),
        "total": len(combined_data),
        "data": combined_data
    }
