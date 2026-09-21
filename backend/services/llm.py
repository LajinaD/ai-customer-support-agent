from dotenv import load_dotenv
import os
from langchain_groq import ChatGroq
from models.intent import UserIntent

load_dotenv()

print("LANGSMITH_TRACING:", os.getenv("LANGSMITH_TRACING"))
print("LANGSMITH_PROJECT:", os.getenv("LANGSMITH_PROJECT"))
print(
    "LANGSMITH_API_KEY loaded:",
    bool(os.getenv("LANGSMITH_API_KEY"))
)

llm = ChatGroq(
    model = "openai/gpt-oss-120b",
    api_key = os.getenv("GROQ_API_KEY"),
    temperature = 0,
)

def get_llm():
    return llm


# def get_intent_llm():

#     llm = get_llm()

#     return llm.with_structured_output(UserIntent)

# The standard way to get structured data from a LLM in LangChain is by using the .with_structured_output() method, which binds a schema directly to the model and automatically returns a parsed object (like a Pydantic model) instead of a raw text string
