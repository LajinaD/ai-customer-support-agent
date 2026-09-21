REFUND_POLICY_DOCUMENT = """
Refund Policy

Customers can request a refund for delivered orders.

Refund Eligibility:
- The order must have a status of Delivered.
- The customer must request the refund within 7 days of delivery.
- Orders that have not been delivered are not eligible for a refund.
- If a refund has already been processed for an order, another refund cannot be requested.

Refund Amount:
- The refundable amount is equal to the original order price.
- Shipping charges are not currently considered separately.

Refund Process:
1. The system checks whether the order exists.
2. The system checks whether the order has been delivered.
3. The system checks whether the refund request is within the 7-day refund window.
4. The system checks whether a refund has already been processed.
5. If all conditions are satisfied, the customer is asked for explicit confirmation.
6. The refund is processed only after the customer confirms.

Important:
The AI assistant must not claim that a refund has been processed unless the refund processing tool successfully completes the operation.
"""