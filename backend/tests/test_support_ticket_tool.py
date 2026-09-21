from tools.support_ticket_tool import create_support_ticket_tool
from models.order import Order
from models.conversation import Conversation


def test_support_ticket_tool():

    result = create_support_ticket_tool.invoke({
        "conversation_id": "TEST-CONVERSATION-001",
        "order_id": "ORD-1008",
        "issue": "Customer says their refund has not arrived.",
        "priority": "High"
    })

    print("\nTool result:")
    print(result)


if __name__ == "__main__":
    test_support_ticket_tool()