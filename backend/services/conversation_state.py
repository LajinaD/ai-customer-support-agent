from sqlalchemy import select

from config.database import SessionLocal
from models.conversation import Conversation


def save_pending_action(
    conversation_id: str,
    action: str,
    data: dict
):

    with SessionLocal() as session:

        statement = select(Conversation).where(
            Conversation.conversation_id == conversation_id
        )

        conversation = session.scalar(statement)

        if conversation:

            conversation.pending_action = action
            conversation.pending_data = data

        else:

            conversation = Conversation(
                conversation_id=conversation_id,
                pending_action=action,
                pending_data=data
            )

            session.add(conversation)

        session.commit()


def update_pending_action(
    conversation_id: str,
    action: str,
    data: dict
):

    with SessionLocal() as session:

        statement = select(Conversation).where(
            Conversation.conversation_id == conversation_id
        )

        conversation = session.scalar(statement)

        if conversation:

            conversation.pending_action = action
            conversation.pending_data = data

        else:

            conversation = Conversation(
                conversation_id=conversation_id,
                pending_action=action,
                pending_data=data
            )

            session.add(conversation)

        session.commit()


def get_pending_action(conversation_id: str):

    with SessionLocal() as session:

        statement = select(Conversation).where(
            Conversation.conversation_id == conversation_id
        )

        conversation = session.scalar(statement)

        if not conversation:
            return None

        if not conversation.pending_action:
            return None

        return {
            "pending_action": conversation.pending_action,
            "data": conversation.pending_data
        }


def clear_pending_action(conversation_id: str):

    with SessionLocal() as session:

        statement = select(Conversation).where(
            Conversation.conversation_id == conversation_id
        )

        conversation = session.scalar(statement)

        if not conversation:
            return

        conversation.pending_action = None
        conversation.pending_data = None

        session.commit()

def ensure_conversation(conversation_id: str):
    with SessionLocal() as session:

        statement = select(Conversation).where(
            Conversation.conversation_id == conversation_id
        )

        conversation = session.scalar(statement)

        if conversation:
            return

        conversation = Conversation(
            conversation_id=conversation_id
        )

        session.add(conversation)
        session.commit()

        return conversation.conversation_id


# Temporary in-memory conversation state.
# Later we will replace this with Redis/PostgreSQL.

# conversation_states = {}

# def save_pending_action(
#     conversation_id: str,
#     action: str,
#     data: dict
# ):
#     conversation_states[conversation_id] = {
#         "pending_action": action,
#         "data": data
#     }


# def update_pending_action(
#     conversation_id: str,
#     action: str,
#     data: dict
# ):
#     conversation_states[conversation_id] = {
#         "pending_action": action,
#         "data": data
#     }


# def get_pending_action(conversation_id: str):

#     return conversation_states.get(conversation_id)


# def clear_pending_action(conversation_id: str):

#     conversation_states.pop(
#         conversation_id,
#         None
#     )