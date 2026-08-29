"""Chat endpoint - main API."""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.core.rag import retrieve_context
from backend.core.llm import generate_response

router = APIRouter()


class ChatRequest(BaseModel):
    message: str
    use_rag: bool = True


class ChatResponse(BaseModel):
    answer: str
    sources: list[dict] = []


@router.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    if not req.message.strip():
        raise HTTPException(status_code=400, detail="message trống")

    sources: list[dict] = []
    context = ""

    if req.use_rag:
        try:
            context, sources = retrieve_context(req.message)
        except Exception as e:
            # Nếu GraphRAG chưa sẵn sàng, fallback không dùng RAG
            context = ""
            sources = []

    try:
        answer = generate_response(
            question=req.message,
            context=context,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM error: {e}")

    return ChatResponse(answer=answer, sources=sources)
