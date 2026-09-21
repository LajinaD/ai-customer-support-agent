from datetime import date
from datetime import datetime

# from data.orders import orders
from data.refund_policy import REFUND_POLICY

from sqlalchemy import select

from config.database import SessionLocal
from models.order import Order
from models.refund import Refund


def find_order(order_id: str):

    with SessionLocal() as session:

        statement = select(Order).where(
            Order.order_id == order_id
        )

        return session.scalar(statement)

def check_refund_eligibility(order_id: str):

    with SessionLocal() as session:

        # Find order from PostgreSQL
        statement = select(Order).where(
            Order.order_id == order_id
        )

        order = session.scalar(statement)

        if not order:
            return {
                "eligible": False,
                "reason": "Order not found",
                "order_id": order_id
            }

        # Guardrail #2:
        # Check whether a refund already exists
        refund_statement = select(Refund).where(
            Refund.order_id == order_id,
            Refund.status == "Refunded"
        )

        existing_refund = session.scalar(
            refund_statement
        )

        if existing_refund:

            return {
                "eligible": False,
                "reason": "Refund has already been processed",
                "order_id": order_id,
                "refund_status": "Refunded"
            }

        # Check whether order is delivered
        if order.status not in REFUND_POLICY["eligible_statuses"]:

            return {
                "eligible": False,
                "reason": "Order has not been delivered yet",
                "order_id": order_id,
                "status": order.status
            }

        delivered_date = order.delivered_date

        if not delivered_date:

            return {
                "eligible": False,
                "reason": "Delivery date is unavailable",
                "order_id": order_id
            }

        today = date.today()

        days_since_delivery = (
            today - delivered_date
        ).days

        refund_window = REFUND_POLICY[
            "refund_window_days"
        ]

        if days_since_delivery > refund_window:

            return {
                "eligible": False,
                "reason": "Refund window has expired",
                "order_id": order_id,
                "days_since_delivery": days_since_delivery,
                "refund_window_days": refund_window
            }

        return {
            "eligible": True,
            "reason": "Order is eligible for refund",
            "order_id": order_id,
            "days_since_delivery": days_since_delivery,
            "refund_window_days": refund_window,
            "refund_amount": order.price
        }

def process_refund(order_id: str):

    with SessionLocal() as session:

        # Find order
        statement = select(Order).where(
            Order.order_id == order_id
        )

        order = session.scalar(statement)

        if not order:

            return {
                "success": False,
                "reason": "Order not found",
                "order_id": order_id
            }

        # Guardrail #2:
        # Prevent duplicate refunds
        refund_statement = select(Refund).where(
            Refund.order_id == order_id,
            Refund.status == "Refunded"
        )

        existing_refund = session.scalar(
            refund_statement
        )

        if existing_refund:

            return {
                "success": False,
                "reason": "Refund has already been processed",
                "order_id": order_id,
                "refund_status": "Refunded"
            }

        # Guardrail #3:
        # Re-check eligibility immediately before processing
        eligibility = check_refund_eligibility(order_id)

        if not eligibility["eligible"]:

            return {
                "success": False,
                "reason": "Refund cannot be processed",
                "eligibility_reason": eligibility["reason"],
                "order_id": order_id
            }

        # Create persistent refund record
        refund = Refund(
            order_id=order_id,
            amount=order.price,
            status="Refunded",
            processed_at=datetime.utcnow()
        )

        session.add(refund)

        session.commit()

        return {
            "success": True,
            "order_id": order_id,
            "refund_status": "Refunded",
            "refund_amount": order.price,
            "message": "Refund processed successfully"
        }

# def find_order(order_id: str):
#     for order in orders:

#         if order["order_id"] == order_id:
#             return order

#     return

# def check_refund_eligibility(order_id: str):

    order = find_order(order_id)

    if not order:

        return {
            "eligible": False,
            "reason": "Order not found",
            "order_id": order_id
        }

    # Guardrail #2:
    # Prevent refund if it has already been processed
    if order.get("refund_status") == "Refunded":

        return {
            "eligible": False,
            "reason": "Refund has already been processed",
            "order_id": order_id,
            "refund_status": "Refunded"
        }

    if order["status"] not in REFUND_POLICY["eligible_statuses"]:
        return {
            "eligible": False,
            "reason": "Order has not been delivered yet",
            "order_id": order_id,
            "status": order["status"]
        }

    delivered_date = order.get("delivered_date")

    if not delivered_date:
        return{
            "eligible": False,
            "reason": "Delivery date is unavailable",
            "order_id": order_id
        }

    delivered_date = date.fromisoformat(delivered_date)

    today = date.today()

    days_since_delivery = (today - delivered_date).days

    refund_window = REFUND_POLICY["refund_window_days"]

    if days_since_delivery > refund_window :
        return {
            "eligible": False,
            "reason": "Refund window has expired",
            "order_id": order_id,
            "days_since_delivery": days_since_delivery,
            "refund_window_days": refund_window
        }

    return {
        "eligible": True,
        "reason": "Order is eligible for refund",
        "order_id": order_id,
        "days_since_delivery": days_since_delivery,
        "refund_window_days": refund_window,
        "refund_amount": order["price"]
    }

# def process_refund(order_id: str):

    # raise Exception("Simulated refund service failure")

    order = find_order(order_id)

    if not order:
        return {
            "success": False,
            "reason": "Order not found",
            "order_id": order_id
        }

    # Guardrail #2:
    # Final protection against duplicate refund
    if order.get("refund_status") == "Refunded":

        return {
            "success": False,
            "reason": "Refund has already been processed",
            "order_id": order_id,
            "refund_status": "Refunded"
        }

    # Safety Check - recheck eligibility before processing refund
    # Guardrail #3:
    eligibility = check_refund_eligibility(order_id)

    if not eligibility["eligible"]:
        return {
            "success": False,
            "reason": "Refund cannot be processed",
            "eligibility_reason": eligibility["reason"],
            "order_id": order_id
        }

    # Process the refund
    order["refund_status"] = "Refunded"

    return {
        "success": True,
        "order_id": order_id,
        "refund_status": "Refunded",
        "refund_amount": order["price"],
        "message": "Refund processed successfully"
    }

