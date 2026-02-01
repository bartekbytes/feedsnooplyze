import feedparser

feed_url = "https://engineering.fb.com/feed/"
feed = feedparser.parse(feed_url)

print(f"Feed Title: {feed.feed.title}")
for entry in feed.entries:
    print(f"Title: {entry.title}")
    print(f"Link: {entry.link}")
    print(f"Published: {entry.published}")
    print(f"Summary: {entry.summary}\n")    