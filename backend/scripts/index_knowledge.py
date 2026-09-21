from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from data.knowledge_base import REFUND_POLICY_DOCUMENT
from services.vector_store import vector_store


document = Document(
    page_content=REFUND_POLICY_DOCUMENT,
    metadata={
        "source": "refund_policy"
    }
)


text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=300,
    chunk_overlap=50
)


chunks = text_splitter.split_documents(
    [document]
)


print(f"Created {len(chunks)} chunks.")

for i, chunk in enumerate(chunks):
    print(f"\n--- Chunk {i} ---")
    print(chunk.page_content)


print("\nIndexing knowledge base...")

ids = [
    f"refund_policy_{i}"
    for i in range(len(chunks))
]

vector_store.add_documents(
    documents=chunks,
    ids=ids
)

print("Knowledge base indexed successfully.")