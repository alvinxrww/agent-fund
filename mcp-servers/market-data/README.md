# Market Data MCP Server

This is an MCP (Model Context Protocol) server that provides market data tools for the Agent Fund pipeline.
It replaces the browser-based scraping method with direct API calls via `yfinance`.

## Tools Exposed

- `get_rsi(ticker, period=14)`: Gets the Relative Strength Index.
- `get_sma(ticker, window=50)`: Gets the Simple Moving Average.
- `get_price(ticker)`: Gets the most recent closing price.
- `get_technical_summary(tickers)`: Generates a complete status summary for multiple tickers at once.

## Setup

1. Make sure you are in the project's root or have an active Python environment.
2. Install the dependencies for this MCP server:
   ```bash
   pip install -r requirements.txt
   ```
   *(Note: This uses `yfinance` so it does not require an Alpaca API key for market data fetching.)*

## Configuration for AI Clients (e.g. Claude Desktop)

To connect this MCP server to a client like Claude Desktop, add the following to your `claude_desktop_config.json` (replacing `<ABSOLUTE_PATH>` with your actual project root path):

```json
{
  "mcpServers": {
    "agent-fund-market-data": {
      "command": "python",
      "args": ["<ABSOLUTE_PATH>\\mcp-servers\\market-data\\server.py"],
      "env": {
        "PYTHONPATH": "<ABSOLUTE_PATH>\\mcp-servers\\market-data"
      }
    }
  }
}
```
