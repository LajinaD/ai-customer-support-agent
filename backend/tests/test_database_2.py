from services.order import (
    order_status,
    order_details,
    shipping_tracking
)


order_ids = [
    "ORD-1001",
    "ORD-1002",
    "ORD-1003",
    "ORD-1004"
]


for order_id in order_ids:

    print("\n==============================")
    print(order_id)
    print("==============================")

    print(order_status(order_id))
    print(order_details(order_id))
    print(shipping_tracking(order_id))