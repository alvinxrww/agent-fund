import time
from typing import Any, Optional, List
from mcp.server.fastmcp import FastMCP
from datetime import datetime, timezone
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from providers.google_rss import fetch_headlines
from analyzer import analyze_sentiment

mcp = FastMCP("agent-fund-news-sentiment")

CACHE_TTL = 900 # 15 minutes caching
cache = {}

def get_from_cache(key: str) -> Optional[Any]:
    if key in cache:
        entry = cache[key]
        if time.time() - entry['timestamp'] < CACHE_TTL:
            return entry['data']
        else:
            del cache[key]
    return None

def set_to_cache(key: str, data: Any):
    cache[key] = {'timestamp': time.time(), 'data': data}

@mcp.tool()
def get_headlines(keywords: List[str], count: int = 5) -> dict:
    """
    Fetches recent news headlines for given topics.
    
    Args:
        keywords: Listed topics to search for. Example: ["inflation", "interest rates"].
        count: Number of headlines per keyword.
    """
    cache_key = f"headlines_{','.join(keywords)}_{count}"
    cached_val = get_from_cache(cache_key)
    if cached_val is not None:
        return cached_val

    results = []
    for keyword in keywords:
        headlines = fetch_headlines(keyword, count)
        results.append({
            "keyword": keyword,
            "headlines": headlines
        })
        
    data = {"results": results, "timestamp": datetime.now(timezone.utc).isoformat()}
    set_to_cache(cache_key, data)
    return data

@mcp.tool()
def get_macro_sentiment(keywords: List[str] = ["inflation", "interest rates", "fed", "crypto regulation", "tariffs"]) -> dict:
    """
    Analyzes recent headlines and returns a single macro sentiment classification string.
    
    Args:
        keywords: Optional topics to analyze. Defaults to macro-economic triggers.
    """
    cache_key = f"sentiment_{','.join(keywords)}"
    cached_val = get_from_cache(cache_key)
    if cached_val is not None:
        return cached_val

    all_headlines_text = []
    for keyword in keywords:
        headlines = fetch_headlines(keyword, count=4)
        for h in headlines:
            all_headlines_text.append(h['title'])
            
    sentiment_result = analyze_sentiment(all_headlines_text)
    sentiment_result["timestamp"] = datetime.now(timezone.utc).isoformat()
    
    set_to_cache(cache_key, sentiment_result)
    return sentiment_result

if __name__ == "__main__":
    mcp.run()
