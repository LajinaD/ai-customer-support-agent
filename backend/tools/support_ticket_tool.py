from langchain_core.tools import tool

from services.support_ticket import create_support_ticket


@tool
def create_support_ticket_tool(
    conversation_id: str,
    issue: str,
    order_id: str | None = None,
    priority: str = "Normal"
):
    """
    Create a support ticket when the customer's issue
    cannot be safely resolved by the AI assistant.
    """

    return create_support_ticket(
        conversation_id=conversation_id,
        issue=issue,
        order_id=order_id,
        priority=priority
    )