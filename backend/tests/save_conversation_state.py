from services.conversation_state import save_pending_action


save_pending_action(
    "PERSISTENCE-TEST-001",
    "refund_confirmation",
    {
        "order_id": "ORD-1004",
        "refund_amount": 1999
    }
)

print("State saved.")