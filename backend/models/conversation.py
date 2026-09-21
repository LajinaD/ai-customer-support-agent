from datetime import datetime

from sqlalchemy import String, DateTime
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from config.database import Base


class Conversation(Base):

    __tablename__ = "conversations"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    conversation_id: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False
    )

    pending_action: Mapped[str | None] = mapped_column(
        String(100)
    )

    pending_data: Mapped[dict | None] = mapped_column(
        JSONB
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