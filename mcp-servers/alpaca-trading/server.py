from mcp.server.fastmcp import FastMCP
from typing import Dict, Any, List
from datetime import datetime, timezone
import os
import sys

from alpaca_trade_api import REST
from alpaca_trade_api.rest import APIError

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from safety import validate_order, root_env_path
from logger import logger

mcp = FastMCP("agent-fund-alpaca-trading")

# Initialize Alpaca client
api_key = os.getenv("APCA_API_KEY_ID")
api_secret = os.getenv("APCA_API_SECRET_KEY")
api_base_url = os.getenv("APCA_API_BASE_URL", "https://paper-api.alpaca.markets")
is_paper = "paper" in api_base_url

try:
    api = REST(api_key, api_secret, api_base_url)
except Exception as e:
    logger.error(f"Failed to initialize Alpaca REST Client: {e}")
    api = None

@mcp.tool()
def get_account() -> dict:
    """Returns the current account status and buying power."""
    try:
        account = api.get_account()
        data = {
            "account_id": account.id,
            "status": getattr(account, "status", "UNKNOWN"),
            "buying_power": float(account.buying_power),
            "cash": float(account.cash),
            "portfolio_value": float(account.portfolio_value),
            "currency": account.currency,
            "is_paper": is_paper
        }
        logger.info(f"get_account called. Portfolio Value: {data['portfolio_value']}")
        return data
    except Exception as e:
        logger.error(f"get_account failed: {e}")
        return {"error": str(e)}

@mcp.tool()
def get_positions() -> dict:
    """Returns all currently held positions."""
    try:
        positions = api.list_positions()
        data = []
        for p in positions:
            data.append({
                "ticker": p.symbol,
                "qty": float(p.qty),
                "avg_entry_price": float(p.avg_entry_price),
                "current_price": float(p.current_price),
                "unrealized_pl": float(p.unrealized_pl),
                "unrealized_pl_pct": float(p.unrealized_plpc) * 100
            })
        logger.info(f"get_positions called. Total positions: {len(data)}")
        return {
            "positions": data,
            "total_positions": len(data)
        }
    except Exception as e:
        logger.error(f"get_positions failed: {e}")
        return {"error": str(e)}

@mcp.tool()
def submit_order(ticker: str, qty: int, side: str, dry_run: bool = True) -> dict:
    """
    Submits a market order for a given ticker or safely simulates it.
    
    Args:
        ticker: The asset ticker symbol (e.g. VOO).
        qty: Number of shares/units to trade.
        side: 'buy' or 'sell'.
        dry_run: (Crucial) Overrides actual execution when True. 
    """
    try:
        side = side.lower()
        # Fetch latest price to validate thresholds
        # Fetch latest price to validate thresholds
        try:
            if "/" in ticker:
                latest_trade = api.get_latest_crypto_trades([ticker])[ticker]
            else:
                latest_trade = api.get_latest_trade(ticker)
            current_price = float(latest_trade.price)
        except Exception as e:
            logger.warning(f"Could not fetch live price for {ticker}: {e}. Fallback to $1.0.")
            current_price = 1.0

        validate_order(ticker, qty, side, current_price)
        
        account = api.get_account()
        current_bp = float(account.buying_power)
        estimated_cost = current_price * qty
        
        if side == "buy" and estimated_cost > current_bp:
             raise ValueError(f"Insufficient buying power. Available: ${current_bp}, Required: ${estimated_cost}")

        if dry_run:
            logger.info(f"DRY RUN submit_order: {side} {qty} {ticker} at ~${current_price}")
            return {
                "dry_run": True,
                "would_execute": {
                    "ticker": ticker,
                    "side": side,
                    "qty": qty,
                    "estimated_cost": estimated_cost,
                    "current_buying_power": current_bp
                },
                "message": "This is a simulation. Set dry_run=False to execute."
            }
        
        # Real execution
        order = api.submit_order(
            symbol=ticker,
            qty=qty,
            side=side,
            type='market',
            time_in_force='gtc'
        )
        
        logger.info(f"SUBMITTED ORDER: {order.id} | {side} {qty} {ticker}")
        return {
            "dry_run": False,
            "order": {
                "order_id": order.id,
                "ticker": ticker,
                "side": side,
                "qty": qty,
                "status": order.status,
                "submitted_at": datetime.now(timezone.utc).isoformat()
            }
        }

    except Exception as e:
        logger.error(f"submit_order failed for {ticker}: {e}")
        return {"error": str(e)}

@mcp.tool()
def close_position(ticker: str, dry_run: bool = True) -> dict:
    """Closes an existing position entirely."""
    try:
        pos = api.get_position(ticker)
        qty_to_close = float(pos.qty)
        current_price = float(pos.current_price)
        estimated_proceeds = qty_to_close * current_price
        
        if dry_run:
             logger.info(f"DRY RUN close_position: {ticker} (Qty: {qty_to_close})")
             return {
                 "dry_run": True,
                 "would_execute": {
                     "ticker": ticker,
                     "qty_to_close": qty_to_close,
                     "estimated_proceeds": estimated_proceeds
                 },
                 "message": "This is a simulation. Set dry_run=False to execute."
             }
             
        order = api.close_position(ticker)
        logger.info(f"CLOSED POSITION: {order.id} | {ticker}")
        return {
            "dry_run": False,
            "closed": {
                "ticker": ticker,
                "qty_closed": qty_to_close,
                "estimated_proceeds": estimated_proceeds
            }
        }
    except Exception as e:
        logger.error(f"close_position failed for {ticker}: {e}")
        return {"error": str(e)}

if __name__ == "__main__":
    mcp.run()
