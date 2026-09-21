from config.database import SessionLocal
from models.support_ticket import SupportTicket

from models.order import Order
from models.conversation import Conversation

def test_support_ticket_model():

    with SessionLocal() as session:

        ticket = SupportTicket(
            ticket_id="TICKET-TEST-001",
            conversation_id="TEST-CONVERSATION-001",
            order_id="ORD-1008",
            issue="Customer has not received their refund.",
            status="Open",
            priority="Normal"
        )

        session.add(ticket)
        session.commit()

        print("Ticket created successfully.")
        print("Ticket ID:", ticket.ticket_id)
        print("Issue:", ticket.issue)
        print("Status:", ticket.status)
        print("Priority:", ticket.priority)


if __name__ == "__main__":
    test_support_ticket_model()