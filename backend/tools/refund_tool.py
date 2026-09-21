from langchain_core.tools import tool

from services.refund import (
    check_refund_eligibility,
    process_refund
)

@tool
def check_refund_eligibility_tool(order_id: str):
    """
    Check whether a specific order is eligible for a refund
    according to the company's refund policy.

    Use this tool before processing any refund.
    """

    return check_refund_eligibility(order_id)

@tool 
def process_refund_tool(order_id: str):
    """
    Process a refund for an eligible order.

    This action changes the refund status of the order.
    Only process a refund when the order is eligible.

    This tool should only be called after the customer
    has explicitly confirmed that they want the refund.
    """
    
    return process_refund(order_id)