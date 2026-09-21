from sqlalchemy import select

from config.database import SessionLocal
from models.order import Order


def find_order(order_id: str):

    with SessionLocal() as session:

        statement = select(Order).where(
            Order.order_id == order_id
        )

        return session.scalar(statement)


def order_status(order_id: str):

    with SessionLocal() as session:

        statement = select(Order).where(
            Order.order_id == order_id
        )

        order = session.scalar(statement)

        if not order:
            return {
                "error": "Order not found",
                "order_id": order_id
            }

        return {
            "order_id": order.order_id,
            "status": order.status,
            "expected_delivery": (
                order.expected_delivery.isoformat()
                if order.expected_delivery
                else None
            ),
            "delivered_date": (
                order.delivered_date.isoformat()
                if order.delivered_date
                else None
            )
        }


def order_details(order_id: str):

    with SessionLocal() as session:

        statement = select(Order).where(
            Order.order_id == order_id
        )

        order = session.scalar(statement)

        if not order:
            return {
                "error": "Order not found",
                "order_id": order_id
            }

        return {
            "order_id": order.order_id,
            "product": order.product,
            "quantity": order.quantity,
            "price": order.price
        }


def shipping_tracking(order_id: str):

    with SessionLocal() as session:

        statement = select(Order).where(
            Order.order_id == order_id
        )

        order = session.scalar(statement)

        if not order:
            return {
                "error": "Order not found",
                "order_id": order_id
            }

        return {
            "order_id": order.order_id,
            "carrier": order.carrier,
            "tracking_number": order.tracking_number,
            "current_location": order.current_location
        }

# from data.orders import orders

# def find_order(order_id: str):
#     for order in orders:
#         if order["order_id"] == order_id:
#             return order

#     return None

# def order_status(order_id: str):

#     order = find_order(order_id)

#     if not order:
#         return {
#             "error": "Order not found",
#             "order_id": order_id
#         }
#     return {
#         "order_id": order["order_id"],
#         "status": order["status"],
#         "expected_delivery": order["expected_delivery"]
#     }

# def order_details(order_id: str):

#     order = find_order(order_id)

#     if not order:
#         return {
#             "error": "Order not found",
#             "order_id": order_id
#         }

#     return {
#         "order_id": order["order_id"],
#         "product": order["product"],
#         "quantity": order["quantity"],
#         "price": order["price"]
#     }

# def shipping_tracking(order_id: str):

#     order = find_order(order_id)

#     if not order:
#         return {
#             "error": "Order not found",
#             "order_id": order_id
#         }

#     return {
#         "order_id": order["order_id"],
#         "carrier": order["carrier"],
#         "tracking_number": order["tracking_number"],
#         "current_location": order["current_location"]
#     }