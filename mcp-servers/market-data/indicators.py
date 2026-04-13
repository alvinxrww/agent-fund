import pandas as pd
import numpy as np

def calculate_rsi(series: pd.Series, period: int = 14) -> float:
    """
    Calculates the Relative Strength Index (RSI) for a pandas Series.
    Uses Wilder's Smoothing method.
    """
    if len(series) < period:
        return 50.0 # Default fallback
    
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).fillna(0)
    loss = (-delta.where(delta < 0, 0)).fillna(0)

    avg_gain = gain.ewm(alpha=1/period, min_periods=period, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1/period, min_periods=period, adjust=False).mean()

    # Avoid division by zero
    rs = avg_gain / avg_loss.replace(0, np.nan)
    rsi = 100 - (100 / (1 + rs))
    rsi = rsi.fillna(100) # If loss is 0, rsi is 100
    
    return round(float(rsi.iloc[-1]), 2) if not pd.isna(rsi.iloc[-1]) else 50.0

def calculate_sma(series: pd.Series, window: int = 50) -> float:
    """
    Calculates the Simple Moving Average (SMA) for a pandas Series.
    """
    if len(series) < window:
        return 0.0
    sma = series.rolling(window=window).mean()
    return round(float(sma.iloc[-1]), 2) if not pd.isna(sma.iloc[-1]) else 0.0

def determine_status(rsi: float) -> str:
    """
    Determines market status based on basic RSI thresholds.
    """
    if rsi > 70:
        return "OVERBOUGHT"
    elif rsi < 30:
        return "OVERSOLD"
    else:
        return "NEUTRAL"
