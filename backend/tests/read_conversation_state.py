from services.conversation_state import get_pending_action


state = get_pending_action(
    "PERSISTENCE-TEST-001"
)

print("Retrieved state:")
print(state)