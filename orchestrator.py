import sys
import os
import json
import importlib.util
from datetime import datetime, timezone
from dotenv import load_dotenv

# Load root .env
load_dotenv()

def load_module_from_path(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.path.insert(0, os.path.dirname(file_path))
    spec.loader.exec_module(module)
    sys.path.pop(0) 
    return module

# Load MCP Servers as modules
market_server = load_module_from_path('market_server', os.path.abspath('mcp-servers/market-data/server.py'))
news_server = load_module_from_path('news_server', os.path.abspath('mcp-servers/news-sentiment/server.py'))
signal_server = load_module_from_path('signal_server', os.path.abspath('mcp-servers/signal-engine/server.py'))
alpaca_server = load_module_from_path('alpaca_server', os.path.abspath('mcp-servers/alpaca-trading/server.py'))
telegram_server = load_module_from_path('telegram_server', os.path.abspath('mcp-servers/telegram-bot/server.py'))

def run_pipeline(dry_run=True, send_telegram=True):
    print("\n" + "="*50)
    print("AGENT FUND: AUTONOMOUS TRADING PIPELINE")
    print("="*50 + "\n")

    # Step 1: Detect Initiation (Already done by user in chat)
    print("[*] Initiating Pipeline Workflow...")

    # Step 2: Obtain Market Data
    tickers = ["BTC/USD", "GLD", "VOO"]
    print(f"[*] Fetching technical summary for {tickers}...")
    try:
        market_summary = market_server.get_technical_summary(tickers)
        market_data = market_summary.get("data", [])
    except Exception as e:
        print(f"Error fetching market data: {e}")
        market_data = []

    # Step 3: Fetch Macro Sentiment
    print("[*] Analyzing macro-economic sentiment...")
    try:
        sentiment_resp = news_server.get_macro_sentiment()
        sentiment_val = sentiment_resp.get("sentiment", "Mixed")
    except Exception as e:
        print(f"Error fetching sentiment: {e}")
        sentiment_val = "Mixed"

    # Step 4: Generate Signals
    print(f"[*] Generating signals using 'rsi_sentiment' strategy (Sentiment: {sentiment_val})...")
    try:
        signals_resp = signal_server.generate_signals(
            market_data=market_data, 
            sentiment=sentiment_val, 
            strategy="rsi_sentiment"
        )
        signals = signals_resp.get("signals", [])
    except Exception as e:
        print(f"Error generating signals: {e}")
        signals = []

    # Step 5: Check Account State
    print("[*] Checking account balance and positions...")
    try:
        account = alpaca_server.get_account()
        positions = alpaca_server.get_positions().get("positions", [])
    except Exception as e:
        print(f"Error fetching account info: {e}")
        account = {}
        positions = []

    # Step 6: Presentation
    summary_text = f"<b>🚀 Agent Fund Pipeline Summary</b>\n"
    summary_text += f"📅 Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    summary_text += f"📊 Sentiment: <b>{sentiment_val}</b>\n\n"
    
    summary_text += "<b>TICKER | RSI | SMA50 | SIGNAL</b>\n"
    for s in signals:
        summary_text += f"`{s['ticker']:<7} | {s['rsi']:<3.1f} | {s['action']}`\n"
    
    summary_text += f"\n💰 Buying Power: ${account.get('buying_power', 0):,.2f}\n"
    summary_text += f"📁 Open Positions: {len(positions)}\n"
    summary_text += f"📁 Use dry run: {dry_run}\n"
    
    if send_telegram:
        print("[*] Pushing summary to Telegram...")
        try:
             telegram_server.send_message(text=summary_text)
        except Exception as e:
             print(f"Telegram Failure: {e}")

    print("\n" + "="*50)
    print("SUMMARY REPORT")
    print("="*50)
    # Use .encode().decode() trick or just replace emojis for console safety
    safe_summary = summary_text.replace("<b>", "").replace("</b>", "").replace("`", "")
    try:
        print(safe_summary)
    except UnicodeEncodeError:
        print(safe_summary.encode('ascii', errors='replace').decode('ascii'))
    print("="*50 + "\n")

    return {
        "signals": signals,
        "account": account,
        "sentiment": sentiment_val
    }

def execute_trades(signals, dry_run=True):
    print(f"[*] Executing trades (Dry Run: {dry_run})...")
    results = []
    for sig in signals:
        action = sig.get('action')
        ticker = sig.get('ticker')
        if action in ["BUY", "SELL"]:
            print(f"  -> Order: {action} 1 {ticker}")
            resp = alpaca_server.submit_order(ticker=ticker, qty=1, side=action, dry_run=dry_run)
            results.append(resp)
        else:
            print(f"  -> Skipping {ticker} (HOLD)")
    return results

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Agent Fund Autonomous Orchestrator")
    parser.add_argument("--live", action="store_true", help="Execute trades with LIVE parameters (dry_run=False). Default is dry-run mode.")
    parser.add_argument("--no-telegram", action="store_true", help="Disable sending Telegram summaries.")
    args = parser.parse_args()

    is_dry_run = not args.live
    use_telegram = not args.no_telegram

    # Run the summary pull
    pip_data = run_pipeline(send_telegram=use_telegram, dry_run=is_dry_run)
    
    # Save results
    with open('orchestration_result.json', 'w') as f:
        json.dump(pip_data, f)

    # Proceed to execution results using the argparse parameter
    signals = pip_data.get("signals", [])
    results = execute_trades(signals, dry_run=is_dry_run)
    
    print("\n" + "="*50)
    print(f"FINAL EXECUTION STATUS (Dry Run: {is_dry_run})")
    print("="*50)
    if not results:
        print("No active trades executed (All seeds were HOLD).")
    else:
        print(json.dumps(results, indent=2))
    print("="*50 + "\n")
