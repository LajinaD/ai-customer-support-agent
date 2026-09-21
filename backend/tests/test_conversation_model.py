from services.conversation_state import (
    save_pending_action,
    update_pending_action,
    get_pending_action,
    clear_pending_action
)


conversation_id = "TEST-CONVERSATION-001"


print("\n--- Save ---")

save_pending_action(
    conversation_id,
    "refund_confirmation",
    {
        "order_id": "ORD-1004",
        "refund_amount": 1999
    }
)

print(get_pending_action(conversation_id))


print("\n--- Update ---")

update_pending_action(
    conversation_id,
    "refund_confirmation",
    {
        "order_id": "ORD-1003",
        "refund_amount": 2999
    }
)

print(get_pending_action(conversation_id))


print("\n--- Clear ---")

clear_pending_action(
    conversation_id
)

print(get_pending_action(conversation_id))