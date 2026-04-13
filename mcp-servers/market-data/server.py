import time
from typing import Any, Optional, List
from mcp.server.fastmcp import FastMCP
from datetime import datetime, timezone
import os
import sys

# Ensure correct module imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from providers.yfinance_provider import get_historical_data, get_current_price
from indicators import calculate_rsi, calculate_sma, determine_status

# Initialize FastMCP Server
mcp = FastMCP("agent-fund-market-data")

# Simple TTL cache for 60 seconds
CACHE_TTL = 60
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
def get_rsi(ticker: str, period: int = 14) -> dict:
    """
    Calculates the Relative Strength Index for a given ticker.
    
    Args:
        ticker: The asset ticker symbol (e.g., BTC/USD, GLD, VOO).
        period: The RSI lookback period in days.
    """
    cache_key = f"rsi_{ticker}_{period}"
    cached_val = get_from_cache(cache_key)
    if cached_val is not None:
        return cached_val
    
    try:
        # Fetch at least enough data days
        fetch_period = f"{max(period * 2, 60)}d"
        df = get_historical_data(ticker, period=fetch_period)
        if df is None:
            return {"error": f"Ticker not found or data indisponible: {ticker}"}
        
        rsi_val = calculate_rsi(df['Close'], period)
        
        result = {
            "ticker": ticker,
            "rsi": rsi_val,
            "period": period,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        set_to_cache(cache_key, result)
        return result
    except Exception as e:
        return {"error": f"Failed to get RSI: {str(e)}"}

@mcp.tool()
def get_sma(ticker: str, window: int = 50) -> dict:
    """
    Calculates the Simple Moving Average for a given ticker.
    
    Args:
        ticker: The asset ticker symbol.
        window: The SMA window in days.
    """
    cache_key = f"sma_{ticker}_{window}"
    cached_val = get_from_cache(cache_key)
    if cached_val is not None:
        return cached_val

    try:
        fetch_period = f"{max(window * 2, 100)}d"
        df = get_historical_data(ticker, period=fetch_period)
        if df is None:
            return {"error": f"Ticker not found or data indisponible: {ticker}"}
        
        sma_val = calculate_sma(df['Close'], window)
        current_price = float(df['Close'].iloc[-1])
        
        result = {
            "ticker": ticker,
            "sma": sma_val,
            "window": window,
            "current_price": round(current_price, 2),
            "price_vs_sma": "above" if current_price > sma_val else "below",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        set_to_cache(cache_key, result)
        return result
    except Exception as e:
        return {"error": f"Failed to get SMA: {str(e)}"}

@mcp.tool()
def get_price(ticker: str) -> dict:
    """
    Returns the current or most recent closing price.
    
    Args:
        ticker: The asset ticker symbol.
    """
    cache_key = f"price_{ticker}"
    cached_val = get_from_cache(cache_key)
    if cached_val is not None:
        return cached_val

    try:
        price = get_current_price(ticker)
        if price is None:
            return {"error": f"Ticker not found or data indisponible: {ticker}"}
        
        result = {
            "ticker": ticker,
            "price": round(price, 2),
            "currency": "USD",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        set_to_cache(cache_key, result)
        return result
    except Exception as e:
        return {"error": f"Failed to get price: {str(e)}"}

@mcp.tool()
def get_technical_summary(tickers: List[str]) -> dict:
    """
    A convenience tool that returns RSI, SMA, and price for a list of tickers.
    
    Args:
        tickers: List of ticker symbols (e.g., ["BTC/USD", "GLD", "VOO"]).
    """
    cache_key = f"summary_{','.join(tickers)}"
    cached_val = get_from_cache(cache_key)
    if cached_val is not None:
        return cached_val

    results = []
    for ticker in tickers:
        try:
            df = get_historical_data(ticker, period="100d")
            if df is not None and not df.empty:
                price = round(float(df['Close'].iloc[-1]), 2)
                rsi = calculate_rsi(df['Close'], 14)
                sma_50 = calculate_sma(df['Close'], 50)
                status = determine_status(rsi)
                
                results.append({
                    "ticker": ticker,
                    "price": price,
                    "rsi": rsi,
                    "sma_50": sma_50,
                    "status": status
                })
            else:
                results.append({
                    "ticker": ticker,
                    "error": "Data unavailable"
                })
        except Exception as e:
             results.append({
                  "ticker": ticker,
                  "error": str(e)
             })

    result = {
        "data": results,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
    set_to_cache(cache_key, result)
    return result

if __name__ == "__main__":
    mcp.run()
