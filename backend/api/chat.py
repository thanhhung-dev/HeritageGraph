"""Chat endpoint - main API."""
import logging

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.core.rag import retrieve_context
from backend.core.llm import generate_response

log = logging.getLogger(__name__)

router = APIRouter()


class ChatRequest(BaseModel):
    message: str
    use_rag: bool = True


class ChatResponse(BaseModel):
    answer: str
    sources: list[dict] = []


# KHÔNG dùng `async def`: generate_response() và retrieve_context() đều là hàm
# đồng bộ chạy nặng (mlx sinh token). Trong `async def` chúng chặn event loop nên
# request thứ hai phải đợi request đầu sinh xong. Endpoint đồng bộ được FastAPI
# tự đẩy sang threadpool.
@router.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    if not req.message.strip():
        raise HTTPException(status_code=400, detail="message trống")

    sources: list[dict] = []
    context = ""

    if req.use_rag:
        try:
            context, sources = retrieve_context(req.message)
        except Exception:
            # Retrieval lỗi -> để context RỖNG chứ không trả lời chay: model đã
            # được train từ chối khi "Nguồn: (không có)". Trả lời không nguồn
            # trong lúc retrieval hỏng chính là cách sinh ra câu bịa tự tin.
            log.exception("retrieval lỗi, trả lời với context rỗng")
            context, sources = "", []

    try:
        answer = generate_response(
            question=req.message,
            context=context,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM error: {e}")

    return ChatResponse(answer=answer, sources=sources)
