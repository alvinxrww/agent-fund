# Alpaca Trading MCP Server

This crucial MCP server replaces `trade_executor.py` and provides explicit execution endpoints to the pipeline via the Alpaca Trade API.

## Safety Focus
- Exposes `submit_order` and `close_position`. 
- **By Default:** Both executing tools have `dry_run=True`. An Agent MUST explicitly pass `dry_run=False` intention to fire actual signals into your Alpaca account.
- Implements strict thresholding preventing order actions scaling over `ALPACA_MAX_ORDER_QTY` parameter inside root `.env`.

## Setup

```bash
venv\Scripts\python.exe -m pip install -r mcp-servers\alpaca-trading\requirements.txt
```

## Configuration inside AI Clients

Add the Server to your configuration file:

```json
{
  "mcpServers": {
    "agent-fund-alpaca-trading": {
      "command": "python",
      "args": ["<ABSOLUTE_PATH_TO_AGENT_FUND>\\mcp-servers\\alpaca-trading\\server.py"],
      "env": {
        "PYTHONPATH": "<ABSOLUTE_PATH_TO_AGENT_FUND>\\mcp-servers\\alpaca-trading"
      }
    }
  }
}
```
