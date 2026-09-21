import numpy as np

from services.embeddings import create_embedding


document = (
    "The customer must request the refund within 7 days of delivery."
)

query = (
    "I received my product 5 days ago and want my money back."
)


document_embedding = create_embedding(document)

query_embedding = create_embedding(query)


similarity = np.dot(
    document_embedding,
    query_embedding
) / (
    np.linalg.norm(document_embedding)
    * np.linalg.norm(query_embedding)
)


print("Semantic similarity:")
print(round(float(similarity), 4))