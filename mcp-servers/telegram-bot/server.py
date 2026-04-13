from mcp.server.fastmcp import FastMCP
from typing import Dict, Any, Optional
import os
import sys
import requests
from dotenv import load_dotenv

# Locates the root .env relative to this sub-directory (mcp-servers/telegram-bot/server.py)
root_env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), ".env")
load_dotenv(root_env_path)

mcp = FastMCP("agent-fund-telegram-bot")

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
DEFAULT_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
API_BASE = f"https://api.telegram.org/bot{BOT_TOKEN}" if BOT_TOKEN else None

@mcp.tool()
def get_latest_messages(limit: int = 5, offset: int = None) -> dict:
    """
    Fetches the latest commands/messages sent to the Telegram bot.
    AI agents can poll this periodically to detect '/run' commands.
    
    Args:
        limit: Max number of messages to return.
        offset: Telegram update offset. Pass last update_id + 1 to only
                receive new messages and acknowledge old ones server-side.
    """
    if not API_BASE:
         return {
             "status": "error",
             "message": "TELEGRAM_BOT_TOKEN is missing in the root .env file. Please add it."
         }
         
    try:
        url = f"{API_BASE}/getUpdates"
        params = {"limit": limit, "timeout": 10}
        if offset is not None:
            params["offset"] = offset
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            if not data.get("ok"):
                return {"status": "error", "message": data.get("description")}
                
            messages = []
            for item in data.get("result", []):
                update_id = item.get("update_id")
                msg = item.get("message", {})
                if "text" in msg:
                    messages.append({
                        "update_id": update_id,
                        "message_id": msg.get("message_id"),
                        "from_id": msg.get("from", {}).get("id"),
                        "text": msg.get("text"),
                        "date": msg.get("date")
                    })
            return {"status": "success", "messages": messages}
        else:
             return {"status": "error", "message": f"HTTP {response.status_code}: {response.text}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@mcp.tool()
def send_message(text: str, chat_id: Optional[str] = None) -> dict:
    """
    Sends a message (like a pipeline summary or approval request) directly to the user's Telegram.
    
    Args:
        text: The message body to send.
        chat_id: Optional. The target user ID. If None, uses TELEGRAM_CHAT_ID from .env.
    """
    if not API_BASE:
         return {
             "status": "error",
             "message": "TELEGRAM_BOT_TOKEN is missing in the root .env file. Please add it."
         }
         
    target_id = chat_id or DEFAULT_CHAT_ID
    if not target_id:
         return {
             "status": "error",
             "message": "No chat_id provided and TELEGRAM_CHAT_ID is missing in the root .env file."
         }
         
    try:
        url = f"{API_BASE}/sendMessage"
        payload = {
            "chat_id": target_id,
            "text": text,
            "parse_mode": "HTML"
        }
        response = requests.post(url, json=payload, timeout=10)
        
        if response.status_code == 200:
             return {"status": "success", "delivered": True}
        else:
             return {"status": "error", "message": f"HTTP {response.status_code}: {response.text}"}
             
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    mcp.run()
