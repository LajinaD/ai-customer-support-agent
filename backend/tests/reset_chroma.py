import chromadb


client = chromadb.PersistentClient(
    path="./chroma_db"
)

try:
    client.delete_collection(
        name="knowledge_base_chunks"
    )
    print("Collection deleted.")
except Exception:
    print("Collection did not exist.")


print("Chroma collection reset.")