from tools.knowledge_tool import search_knowledge_tool


result = search_knowledge_tool.invoke({"query": "How many days do I have to request a refund?"})

print("Knowledge tool result:")
print(result)