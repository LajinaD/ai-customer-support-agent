from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from config.database import Base


class Customer(Base):

    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    name: Mapped[str | None] = mapped_column(
        String(100)
    )

    email: Mapped[str | None] = mapped_column(
        String(255)
    )