import os

from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

load_dotenv()


embeddings = OpenAIEmbeddings(
    model="liquid/lfm-2.5-embedding-350m:free",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
    check_embedding_ctx_length=False
)


vector_store = Chroma(
    collection_name="knowledge_base_chunks",
    embedding_function=embeddings,
    persist_directory="./chroma_db"
)