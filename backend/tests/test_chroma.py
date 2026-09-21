import chromadb

client = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = client.get_or_create_collection(
    name="knowledge_base"
)

collection.add(
    ids=["refund-1"],
    documents=[
        "The customer must request the refund within 7 days of delivery."
    ]
)

results = collection.query(
    query_texts=[
        "I received my product 5 days ago and want my money back."
    ],
    n_results=1
)

print("Retrieved documents:")
print(results["documents"])