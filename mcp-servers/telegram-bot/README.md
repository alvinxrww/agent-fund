# Telegram Bot MCP Server

This MCP server acts as the asynchronous communication link between the user and the local Agent Fund execution pipeline. It replaces manual local terminal interactions with remote commands.

## Requirements

1. Acquire a Bot Token from the [@BotFather](https://t.me/botfather) on Telegram.
2. Provide your target Chat ID.
3. Open your project root `d:\Work\agent-fund\.env` and append the variables:
```env
TELEGRAM_BOT_TOKEN="your_bot_token_here"
TELEGRAM_CHAT_ID="your_personal_chat_id_here"
```

## Setup

Navigate to your workspace root and run the locked dependency injection:
```bash
venv\Scripts\python.exe -m pip install -r mcp-servers\telegram-bot\requirements.txt
```

## Tools Exposed

- `get_latest_messages()`: Native HTTP polling to read inbound commands without locking a thread.
- `send_message(text, chat_id)`: Pushes summaries out to the user's pocket.

## Configuration for AI Clients

Add the Server to your configuration file:

```json
{
  "mcpServers": {
    "agent-fund-telegram-bot": {
      "command": "python",
      "args": ["<ABSOLUTE_PATH_TO_AGENT_FUND>\\mcp-servers\\telegram-bot\\server.py"],
      "env": {
        "PYTHONPATH": "<ABSOLUTE_PATH_TO_AGENT_FUND>\\mcp-servers\\telegram-bot"
      }
    }
  }
}
```
