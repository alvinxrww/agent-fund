from typing import Dict, Any, List

def apply_strategy(market_data: List[Dict[str, Any]], sentiment: str = None) -> List[Dict[str, Any]]:
    """
    Applies the basic RSI quantitative strategy to produce signals.
    BUY when RSI < 30, SELL when RSI > 70, else HOLD.
    """
    signals = []
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

        if rsi < 30:
            action = "BUY"
            reasoning = f"RSI is {rsi} (below 30), indicating oversold."
        elif rsi > 70:
            action = "SELL"
            reasoning = f"RSI is {rsi} (above 70), indicating overbought."
        else:
            action = "HOLD"
            reasoning = f"RSI is {rsi} (neutral)."

        signals.append({
            "ticker": ticker,
            "action": action,
            "rsi": rsi,
            "reasoning": reasoning
        })

    return signals
