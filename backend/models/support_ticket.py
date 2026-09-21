from datetime import datetime

from sqlalchemy import String, Text, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from config.database import Base


class SupportTicket(Base):
    __tablename__ = "support_tickets"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    ticket_id: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False
    )

    conversation_id: Mapped[str | None] = mapped_column(
        ForeignKey("conversations.conversation_id")
    )

    order_id: Mapped[str | None] = mapped_column(
        ForeignKey("orders.order_id")
    )

    issue: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="Open"
    )

    priority: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="Normal"
    )

    created_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )