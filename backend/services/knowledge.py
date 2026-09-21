from services.vector_store import vector_store


def search_knowledge(query: str):
    results = vector_store.similarity_search(
        query,
        k=3
    )

    return [
        {
            "text": document.page_content,
            "metadata": document.metadata
        }
        for document in results
    ]