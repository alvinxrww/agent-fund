from typing import List, Dict, Any

POSITIVE_KEYWORDS = ["growth", "rally", "dovish", "easing", "bull", "surge", "gain", "high", "jump", "positive", "strong"]
NEGATIVE_KEYWORDS = ["recession", "crash", "hawkish", "tariff", "bear", "plunge", "loss", "low", "drop", "negative", "weak", "inflation", "hike", "fear", "tension"]

def analyze_sentiment(headlines: List[str]) -> Dict[str, Any]:
    positive_count = 0
    negative_count = 0
    neutral_count = 0
    
    for headline in headlines:
        headline_lower = headline.lower()
        is_pos = any(word in headline_lower for word in POSITIVE_KEYWORDS)
        is_neg = any(word in headline_lower for word in NEGATIVE_KEYWORDS)
        
        if is_pos and not is_neg:
            positive_count += 1
        elif is_neg and not is_pos:
            negative_count += 1
        elif is_pos and is_neg:
            # If both, treat as negative conservatively for risk management
            negative_count += 1
        else:
            neutral_count += 1
            
    total = len(headlines)
    if total == 0:
        return {
            "sentiment": "Mixed",
            "confidence": "low",
            "reasoning": "No headlines provided.",
            "headline_count_analyzed": 0,
            "positive_count": 0,
            "negative_count": 0,
            "neutral_count": 0
        }
        
    neg_ratio = negative_count / total
    pos_ratio = positive_count / total
    
    if neg_ratio > 0.4:  # 40% negative threshold for Risk-Off
        sentiment = "Risk-Off"
    elif pos_ratio > 0.4:
        sentiment = "Risk-On"
    else:
        sentiment = "Mixed"
        
    return {
        "sentiment": sentiment,
        "confidence": "medium",
        "reasoning": f"Analyzed {total} headlines. Positive: {positive_count}, Negative: {negative_count}.",
        "headline_count_analyzed": total,
        "positive_count": positive_count,
        "negative_count": negative_count,
        "neutral_count": neutral_count
    }
