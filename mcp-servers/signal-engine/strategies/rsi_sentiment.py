from typing import Dict, Any, List

def apply_strategy(market_data: List[Dict[str, Any]], sentiment: str = None) -> List[Dict[str, Any]]:
    """
    Applies an RSI strategy adjusted by macro sentiment.
    In Risk-Off, requires RSI < 25 for BUY, and SELL threshold drops to 65.
    In Risk-On, requires RSI > 75 for SELL, and BUY threshold rises to 35.
    """
    signals = []
    
    # Default thresholds
    buy_thresh = 30
    sell_thresh = 70
    
    if sentiment == "Risk-Off":
        buy_thresh = 25
        sell_thresh = 65
    elif sentiment == "Risk-On":
        buy_thresh = 35
        sell_thresh = 75

    for item in market_data:
        ticker = item.get("ticker", "UNKNOWN")
        rsi = item.get("rsi")

        if rsi is None:
            signals.append({
                "ticker": ticker,
                "action": "HOLD",
                "reasoning": "Missing RSI data."
            })
            continue

        if rsi < buy_thresh:
            action = "BUY"
            reasoning = f"RSI is {rsi} (below {buy_thresh} adjusted for {sentiment}), indicating oversold."
        elif rsi > sell_thresh:
            action = "SELL"
            reasoning = f"RSI is {rsi} (above {sell_thresh} adjusted for {sentiment}), indicating overbought."
        else:
            action = "HOLD"
            reasoning = f"RSI is {rsi} (between {buy_thresh} and {sell_thresh})."

        signals.append({
            "ticker": ticker,
            "action": action,
            "rsi": rsi,
            "reasoning": reasoning
        })

    return signals
