"""FastAPI app chính cho chatbot văn hóa Đà Nẵng - Huế."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api import chat, graph, health

app = FastAPI(
    title="Chatbot Văn hóa Đà Nẵng - Huế",
    description="RAG + LoRA fine-tuned Qwen2.5, chạy 100% local",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Next.js dev
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/api")
app.include_router(chat.router, prefix="/api")
app.include_router(graph.router, prefix="/api")


@app.get("/")
async def root():
    return {
        "name": "Chatbot Văn hóa Đà Nẵng - Huế",
        "docs": "/docs",
        "health": "/api/health",
        "graph": "/api/graph/stats",
    }
