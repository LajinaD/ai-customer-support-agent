from langchain_core.documents import Document

from services.vector_store import vector_store


documents = [
    Document(
        page_content=(
            "The customer must request the refund "
            "within 7 days of delivery."
        ),
        metadata={
            "source": "refund_policy"
        }
    ),
    Document(
        page_content=(
            "Orders that have not been delivered "
            "are not eligible for a refund."
        ),
        metadata={
            "source": "refund_policy"
        }
    ),
    Document(
        page_content=(
            "The refundable amount is equal to "
            "the original order price."
        ),
        metadata={
            "source": "refund_policy"
        }
    )
]


print("Embedding documents and storing them in Chroma...")

vector_store.add_documents(documents)

print("Indexing complete!")


query = (
    "I received my product 5 days ago "
    "and want my money back."
)

print(f"\nSearching for: {query}")

results = vector_store.similarity_search(
    query,
    k=2
)


print("\n--- Results ---")

for doc in results:
    print("\nContent:")
    print(doc.page_content)

    print("Metadata:")
    print(doc.metadata)