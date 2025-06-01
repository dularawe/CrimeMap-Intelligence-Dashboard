import feedparser

# RSS feed URL
rss_url = "https://www.defense.gov/DesktopModules/ArticleCS/RSS.ashx?max=10&ContentType=1&Site=945"

# Parse the feed
feed = feedparser.parse(rss_url)

# Display basic feed info
print(" Feed Title:", feed.feed.get("title", "Unknown Feed"))
print(" Total Articles:", len(feed.entries))


for i, entry in enumerate(feed.entries[:10], start=1):
    print(f"\n#{i} 🔹 Title: {entry.get('title', 'No Title')}")
    print(f"🔗 Link: {entry.get('link', '')}")
    print(f" Description: {entry.get('description', '')[:200]}...")
