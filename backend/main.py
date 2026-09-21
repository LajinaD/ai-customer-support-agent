from fastapi import FastAPI
from routers import chat

app = FastAPI(
    title = "CustomerSupport",
    version = "1.0.0",
    description = "AI Customer Support Agent"
)

@app.get("/")
def home():
    return{
        "message": "Welcome to Customer Support Agent"
    }

@app.get("/health")
def health():
    return {
        "status": "healthy"
    }

app.include_router(chat.router)