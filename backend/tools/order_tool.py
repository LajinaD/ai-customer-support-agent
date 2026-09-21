from langchain_core.tools import tool
from services.order import order_status, order_details, shipping_tracking


@tool
def get_order_status(order_id: str):
    """Get the current status and expected delivery date of an order."""
    return order_status(order_id)
    
@tool
def get_order_details(order_id: str):
    """Get the products, quantity, and price for an order."""
    return order_details(order_id)
    
@tool
def get_shipping_tracking(order_id: str):
    """Get the shipping carrier, tracking number, and current location of an order."""
    return shipping_tracking(order_id)
    