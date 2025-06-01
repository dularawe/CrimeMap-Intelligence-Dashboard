import feedparser
from ml_server.classifier import is_crime_related
from ml_server.geolocator import extract_location

def fetch_rss_news():
    feeds = [
        "https://www.adaderana.lk/rss.php",
        "https://rss.cnn.com/rss/cnn_world.rss",
        "https://feeds.bbci.co.uk/news/world/rss.xml",
        "https://www.dailynews.lk/feed/",
        "https://www.dinamina.lk/feed/",
        "https://www.news.lk/news?format=feed",
        "https://www.defense.gov/DesktopModules/ArticleCS/RSS.ashx?max=10&ContentType=1&Site=945",
        "http://localhost:8080/news.xml"
    ]

    events = []

    for url in feeds:
        try:
            rss = feedparser.parse(url)
            for entry in rss.entries:
                if is_crime_related(entry.title):
                    location = extract_location(entry.title + " " + entry.get("description", ""))
                    if location:
                        events.append({
                            "title": entry.title,
                            "description": entry.get("description", ""),
                            "category": "crime",
                            "latitude": location.latitude,
                            "longitude": location.longitude,
                            "source_url": entry.link
                        })
        except Exception as e:
            print(f" Error parsing {url}: {e}")

    return events
