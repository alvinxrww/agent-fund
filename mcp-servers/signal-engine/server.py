from mcp.server.fastmcp import FastMCP
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from strategies import rsi_basic, rsi_sentiment

mcp = FastMCP("agent-fund-signal-engine")

@mcp.tool()
def get_available_strategies() -> dict:
    """
    Lists all available signal generation strategies.
    """
    return {
        "strategies": [
            {
                "name": "rsi_basic",
                "description": "BUY when RSI < 30 (oversold), SELL when RSI > 70 (overbought), else HOLD.",
                "parameters": ["market_data"]
            },
            {
                "name": "rsi_sentiment",
                "description": "Like rsi_basic, but adjusts thresholds based on macro sentiment. In Risk-Off environments, tighten the BUY threshold to RSI < 25.",
                "parameters": ["market_data", "sentiment"]
            }
        ]
    }

@mcp.tool()
def generate_signals(market_data: List[Dict[str, Any]], sentiment: Optional[str] = None, strategy: str = "rsi_basic") -> dict:
    """
    Generates quantitative trade signals using a specific strategy.
    
    Args:
        market_data: The technical data for each asset (must include ticker and rsi).
        sentiment: Overall macro sentiment ('Risk-On', 'Risk-Off', 'Mixed').
        strategy: Which strategy to apply.
    """
    if strategy == "rsi_basic":
        signals = rsi_basic.apply_strategy(market_data, sentiment)
    elif strategy == "rsi_sentiment":
        signals = rsi_sentiment.apply_strategy(market_data, sentiment)
    else:
        return {"error": f"Strategy not found: {strategy}"}

    return {
        "signals": signals,
        "strategy_used": strategy,
        "sentiment_applied": sentiment,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

if __name__ == "__main__":
    mcp.run()
