import uuid

from sqlalchemy import select

from config.database import SessionLocal
from models.support_ticket import SupportTicket


def create_support_ticket(
    conversation_id: str,
    issue: str,
    order_id: str | None = None,
    priority: str = "Normal"
):
    with SessionLocal() as session:

        ticket_id = f"TICKET-{uuid.uuid4().hex[:8].upper()}"

        ticket = SupportTicket(
            ticket_id=ticket_id,
            conversation_id=conversation_id,
            order_id=order_id,
            issue=issue,
            status="Open",
            priority=priority
        )

        session.add(ticket)
        session.commit()
        session.refresh(ticket)

        return {
            "success": True,
            "ticket_id": ticket.ticket_id,
            "conversation_id": ticket.conversation_id,
            "order_id": ticket.order_id,
            "issue": ticket.issue,
            "status": ticket.status,
            "priority": ticket.priority,
        }


def get_support_ticket(ticket_id: str):
    with SessionLocal() as session:

        statement = select(SupportTicket).where(
            SupportTicket.ticket_id == ticket_id
        )

        ticket = session.scalar(statement)

        if not ticket:
            return {
                "success": False,
                "reason": "Support ticket not found",
                "ticket_id": ticket_id
            }

        return {
            "success": True,
            "ticket_id": ticket.ticket_id,
            "conversation_id": ticket.conversation_id,
            "order_id": ticket.order_id,
            "issue": ticket.issue,
            "status": ticket.status,
            "priority": ticket.priority,
        }