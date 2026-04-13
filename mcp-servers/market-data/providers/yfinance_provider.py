import yfinance as yf
import pandas as pd
from typing import Optional

def get_historical_data(ticker: str, period: str = "1y", interval: str = "1d") -> Optional[pd.DataFrame]:
    """
    Fetches historical data for a given ticker using yfinance.
    """
    try:
        # yfinance uses symbols like BTC-USD instead of BTC/USD
        formatted_ticker = ticker.replace("/", "-")
        stock = yf.Ticker(formatted_ticker)
        df = stock.history(period=period, interval=interval)
        if df.empty:
            return None
        return df
    except Exception as e:
        # Log or handle exception properly if needed
        return None

def get_current_price(ticker: str) -> Optional[float]:
    """
    Fetches the latest closing price for a ticker.
    """
    df = get_historical_data(ticker, period="5d") # Get recent data to ensure we have a current close
    if df is not None and not df.empty:
        return float(df['Close'].iloc[-1])
    return None
