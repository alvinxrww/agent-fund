# 🤖 Agent Fund: Autonomous Quant Pipeline

Agent Fund is an end-to-end autonomous trading system that leverages agentic AI to perform market analysis and execute trades based on quantitative signals. It is designed to bridge the gap between high-level market sentiment and programmatic execution.

## 🏗️ Architecture

The pipeline consists of three primary layers:

### 1. Market Scout (Analysis Layer)
Located in `.agent/skills/market-scout/`, this module performs visual and sentiment analysis on key assets (BTC, GLD, VOO). It generates a `market_pulse.md` report containing technical indicators like RSI.

### 2. Quant Engine (Signal Layer)
- **`engine/signal_generator.py`**: A Python script that parses the `market_pulse.md` data using regex and applies a quantitative RSI-based logic (Overbought > 70, Oversold < 30) to generate actionable trade signals in `engine/signal.json`.

### 3. Portfolio Manager (Execution Layer)
- **`engine/trade_executor.py`**: Uses the Alpaca Trade API to execute market orders based on the generated signals.
- **Safety Protocol**: As defined in `CLAUDE.md`, the AI Portfolio Manager must summarize all pending trades and wait for an explicit **"Y"** approval from the user before triggering the execution script.

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- Alpaca Trade API keys (Paper or Live)

### Setup
1. **Clone the repository.**
2. **Create a virtual environment:**
   ```cmd
   python -m venv venv
   ```
3. **Install dependencies:**
   ```cmd
   venv\Scripts\pip install -r requirements.txt
   ```
4. **Configure Environment Variables:**
   Create a `.env` file in the root directory (never commit this) with the following:
   ```env
   APCA_API_KEY_ID=your_key_here
   APCA_API_SECRET_KEY=your_secret_here
   APCA_API_BASE_URL=https://paper-api.alpaca.markets
   ```

## 🛠️ Usage

The entire pipeline is orchestrated via the **`/run-pipeline`** workflow. 

Executing the workflow will:
1. Trigger the **Market Scout** to analyze current market conditions.
2. Run the **Signal Generator** to convert analysis into data.
3. Call the **Portfolio Manager** to present a trade summary for your approval.
4. Execute trades via **Alpaca** upon your "Y" confirmation.

## ⚠️ Disclaimer
This project is for educational and research purposes. Automated trading carries significant risk. Always use paper trading accounts first to verify logic before even considering live capital.
