import sys

# Ensure UTF-8 output for emojis
if hasattr(sys.stdout, 'reconfigure') and sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

import json
import os
from dotenv import load_dotenv
from alpaca_trade_api import REST, TimeFrame

# Load the paper trading keys from .env
load_dotenv()
API_KEY = os.getenv('APCA_API_KEY_ID')
SECRET_KEY = os.getenv('APCA_API_SECRET_KEY')
BASE_URL = os.getenv('APCA_API_BASE_URL')

alpaca = REST(API_KEY, SECRET_KEY, BASE_URL, api_version='v2')

SIGNAL_PATH = "engine/signal.json"

def execute_signals():
    try:
        with open(SIGNAL_PATH, 'r') as file:
            signals = json.load(file)
            
        print("🔍 Scanning signals for execution...")
        
        for ticker, data in signals.items():
            action = data.get("action")
            
            if action == "BUY":
                print(f"📈 Executing BUY for {ticker} (RSI: {data.get('rsi')})")
                # Buy 1 share/unit as a safe test
                alpaca.submit_order(
                    symbol=ticker,
                    qty=1,
                    side='buy',
                    type='market',
                    time_in_force='gtc'
                )
            elif action == "SELL":
                print(f"📉 Executing SELL for {ticker} (RSI: {data.get('rsi')})")
                # Liquidate the position
                try:
                    alpaca.close_position(ticker)
                except Exception as e:
                    print(f"   Note: Could not sell {ticker}. Not currently holding any.")
            else:
                print(f"⏸️ HOLDing {ticker}")
                
        print("✅ Execution run complete.")
                
    except FileNotFoundError:
        print("❌ signal.json not found. Run the Quant Engine first.")
    except Exception as e:
        print(f"⚠️ API Error: {e}")

if __name__ == "__main__":
    execute_signals()