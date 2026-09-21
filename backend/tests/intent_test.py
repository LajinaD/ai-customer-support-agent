from services.intent import detect_intent


tests = [

    "I want a refund for ORD-1004",

    "Where is my order ORD-1001?",

    "Tell me what product I bought in ORD-1001",

    "Can you give me the tracking information for ORD-1001?",

    "Hi, how are you?"

]


for text in tests:

    result = detect_intent(text)

    print("\nUser:", text)

    print("Intent:", result.intent)

    print("Order ID:", result.order_id)