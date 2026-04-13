import os
from dotenv import load_dotenv

# Locates the root .env relative to this sub-directory (mcp-servers/alpaca-trading/safety.py)
root_env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), ".env")
load_dotenv(root_env_path)

MAX_ORDER_QTY = int(os.getenv("ALPACA_MAX_ORDER_QTY", "5"))
MAX_ORDER_VALUE = float(os.getenv("ALPACA_MAX_ORDER_VALUE", "5000.0"))

def validate_order(ticker: str, qty: int, side: str, estimated_price: float) -> bool:
    """
    Validates if an order passes the strict safety constraints.
    Returns True if valid, raises ValueError if invalid.
    """
    if qty <= 0:
        raise ValueError(f"Quantity must be positive. Received: {qty}")
    
    if qty > MAX_ORDER_QTY:
        raise ValueError(f"Order quantity {qty} exceeds safety limit of {MAX_ORDER_QTY}")
        
    estimated_value = qty * estimated_price
    if estimated_value > MAX_ORDER_VALUE:
        raise ValueError(f"Order estimated value ${estimated_value} exceeds safety limit of ${MAX_ORDER_VALUE}")
        
    if side not in ["buy", "sell"]:
        raise ValueError(f"Side must be 'buy' or 'sell'. Received: {side}")
        
    return True
