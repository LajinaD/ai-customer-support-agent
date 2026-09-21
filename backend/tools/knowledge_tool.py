from langchain_core.tools import tool

from services.knowledge import search_knowledge


@tool
def search_knowledge_tool(query: str):
    """
    Search the customer support knowledge base for
    policies and general support information.
    """

    results = search_knowledge(query)

    if not results:
        return {
            "found": False,
            "results": []
        }

    return {
        "found": True,
        "results": results
    }