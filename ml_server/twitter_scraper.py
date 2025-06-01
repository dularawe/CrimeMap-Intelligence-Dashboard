import tweepy
from ml_server.classifier import is_crime_related
from ml_server.geolocator import extract_location

def fetch_tweets():
    client = tweepy.Client(bearer_token="AAAAAAAAAAAAAAAAAAAAAA5G2AEAAAAAdGmCYF0YkMTjhU4DBMy7tAh92rw%3Dnoaj4MbId5L21qofjy9TCjdh2e4PBppw9buEW5voX9n8p1KKeX")
    query = "terror OR murder OR bomb OR gunfire OR attack -is:retweet lang:en"
    tweets = client.search_recent_tweets(query=query, max_results=10)

    events = []
    for tweet in tweets.data:
        if is_crime_related(tweet.text):
            location = extract_location(tweet.text)
            if location:
                events.append({
                    "title": tweet.text[:50],
                    "description": tweet.text,
                    "category": "crime",
                    "latitude": location.latitude,
                    "longitude": location.longitude,
                    "source_url": f"https://twitter.com/i/web/status/{tweet.id}"
                })
    return events
