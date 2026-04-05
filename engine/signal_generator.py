import json
import re
import os
from datetime import datetime

# Define where Antigravity saves the pulse data
ARTIFACT_PATH = r"d:\Work\agent-fund\market_pulse.md"
OUTPUT_SIGNAL_PATH = "engine/signal.json"

def parse_artifact(md_content):
    """Extracts ticker and RSI using regex from the Markdown table."""
    signals = {}
    
    # Looking for lines like: | BTCUSD | 45.5 | ...
    # This is a basic parser; you can make this more robust with an LLM call later
    rows = re.findall(r'\|\s*([A-Z]+)\s*\|\s*([\d.]+)\s*\|', md_content)
    
    for ticker, rsi_str in rows:
        rsi = float(rsi_str)
        action = "HOLD"
        
        # Core Quantitative Logic
        if rsi < 30:
            action = "BUY"
        elif rsi > 70:
            action = "SELL"
            
        signals[ticker] = {
            "action": action,
            "rsi": rsi,
            "timestamp": datetime.now().isoformat()
        }
        
    return signals

def generate_signal():
    try:
        with open(ARTIFACT_PATH, 'r') as file:
            content = file.read()
            
        trade_signals = parse_artifact(content)
        
        with open(OUTPUT_SIGNAL_PATH, 'w') as out_file:
            json.dump(trade_signals, out_file, indent=4)
            
        print(f"✅ Signal generated successfully: {trade_signals}")
        
    except FileNotFoundError:
        print("❌ Waiting for Antigravity to generate the latest artifact.")

if __name__ == "__main__":
    generate_signal()