# News & Sentiment MCP Server

This is an MCP server that provides structured macroeconomic sentiment tools for the Agent Fund pipeline.
It replaces manual/visual browsing of news websites by exposing a structured polling system.

## Tools Exposed

- `get_headlines(keywords, count=5)`: Fetches top recent headlines per keyword.
- `get_macro_sentiment(keywords)`: Aggregates and returns a single macro sentiment rating (`Risk-On`, `Risk-Off`, `Mixed`).

## Setup

Use the project's main virtual environment and the explicitly managed dependency rules:
```bash
venv\Scripts\python.exe -m pip install -r mcp-servers\news-sentiment\requirements.txt
```

## Configuration for AI Clients

In your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "agent-fund-news-sentiment": {
      "command": "python",
      "args": ["<ABSOLUTE_PATH_TO_AGENT_FUND>\\mcp-servers\\news-sentiment\\server.py"],
      "env": {
        "PYTHONPATH": "<ABSOLUTE_PATH_TO_AGENT_FUND>\\mcp-servers\\news-sentiment"
      }
    }
  }
}
```
