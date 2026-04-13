import feedparser
import urllib.parse
from typing import List, Dict

def fetch_headlines(keyword: str, count: int = 5) -> List[Dict[str, str]]:
    """
    Fetches headlines from Google News RSS for a specific keyword.
    """
    encoded_query = urllib.parse.quote(keyword)
    url = f"https://news.google.com/rss/search?q={encoded_query}&hl=en-US&gl=US&ceid=US:en"
    
    try:
        feed = feedparser.parse(url)
        results = []
        for entry in feed.entries[:count]:
            # The title often includes the source at the end " - Source Name"
            title = entry.title
            
            results.append({
                "title": title,
                "source": entry.source.title if hasattr(entry, 'source') else "Google News",
                "url": getattr(entry, 'link', ''),
                "published": getattr(entry, 'published', 'Unknown')
            })
        return results
    except Exception:
        return []
