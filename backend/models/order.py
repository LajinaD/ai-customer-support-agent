from datetime import date

from sqlalchemy import String, Integer, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from config.database import Base


class Order(Base):

    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    order_id: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False
    )

    customer_id: Mapped[int | None] = mapped_column(
        ForeignKey("customers.id")
    )

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    expected_delivery: Mapped[date | None] = mapped_column(
        Date
    )

    product: Mapped[str | None] = mapped_column(
        String(255)
    )

    quantity: Mapped[int | None] = mapped_column(
        Integer
    )

    price: Mapped[int | None] = mapped_column(
        Integer
    )

    carrier: Mapped[str | None] = mapped_column(
        String(100)
    )

    tracking_number: Mapped[str | None] = mapped_column(
        String(100)
    )

    current_location: Mapped[str | None] = mapped_column(
        String(255)
    )

    delivered_date: Mapped[date | None] = mapped_column(
        Date
    )