from services.knowledge import search_knowledge


query = "I received my product 5 days ago and want my money back."

results = search_knowledge(query)

print("Knowledge search results:")

for result in results:
    print("\nText:")
    print(result["text"])

    print("Metadata:")
    print(result["metadata"])