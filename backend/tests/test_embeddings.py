from services.embeddings import create_embedding


text = "The customer can request a refund within 7 days of delivery."

embedding = create_embedding(text)

print("Embedding created successfully.")
print("Vector dimensions:", len(embedding))
print("First 5 values:", embedding[:5])