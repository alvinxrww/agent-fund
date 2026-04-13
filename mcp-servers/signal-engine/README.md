# Signal Engine MCP Server

This MCP server replaces the `signal_generator.py` execution script. 
It receives structured technical data and applies algorithmic thresholds to produce trade signals.

## Tools Exposed

- `get_available_strategies()`: Returns the configured strategies that the AI Agent can invoke.
- `generate_signals(market_data, sentiment, strategy="rsi_basic")`: Analyzes the data and generates an array of actions.

## Setup

Navigate to your workspace root and use the managed virtual environment to install the required dependencies (strictly version matched against the pipeline):

```bash
venv\Scripts\python.exe -m pip install -r mcp-servers\signal-engine\requirements.txt
```

## Configuration for AI Clients

Add the Server to your configuration file:

```json
{
  "mcpServers": {
    "agent-fund-signal-engine": {
      "command": "python",
      "args": ["<ABSOLUTE_PATH_TO_AGENT_FUND>\\mcp-servers\\signal-engine\\server.py"],
      "env": {
        "PYTHONPATH": "<ABSOLUTE_PATH_TO_AGENT_FUND>\\mcp-servers\\signal-engine"
      }
    }
  }
}
```
