from services.llm import get_intent_llm


intent_llm = get_intent_llm()


def detect_intent(user_input: str):

    messages = [

        (
            "system",
            """
            You are an intent classification system
            for a customer support application.

            Identify what the customer wants.

            Allowed intents:

            - refund
            - order_status
            - order_details
            - shipping_tracking
            - general

            Extract the order ID if one is present.

            Order IDs follow this format:

            ORD-XXXX

            If there is no order ID, return null.

            Do not invent an order ID.
            """
        ),

        (
            "user",
            user_input
        )
    ]

    return intent_llm.invoke(messages)