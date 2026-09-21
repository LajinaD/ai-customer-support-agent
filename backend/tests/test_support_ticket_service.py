from services.support_ticket import (
    create_support_ticket,
    get_support_ticket,
)

from models.order import Order
from models.conversation import Conversation


def test_create_support_ticket():

    result = create_support_ticket(
        conversation_id="TEST-CONVERSATION-001",
        order_id="ORD-1008",
        issue="Customer has not received their refund.",
        priority="High"
    )

    print("\nCreated ticket:")
    print(result)

    ticket_id = result["ticket_id"]

    fetched = get_support_ticket(ticket_id)

    print("\nFetched ticket:")
    print(fetched)


if __name__ == "__main__":
    test_create_support_ticket()