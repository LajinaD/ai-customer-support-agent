from datetime import datetime

from sqlalchemy import String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from config.database import Base


class Refund(Base):

    __tablename__ = "refunds"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    order_id: Mapped[str] = mapped_column(
        ForeignKey("orders.order_id"),
        nullable=False
    )

    amount: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    created_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    processed_at: Mapped[datetime | None] = mapped_column(
        DateTime
    )