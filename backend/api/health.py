"""Health check endpoint."""
from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health():
    return {
        "status": "ok",
        "model_loaded": True,  # TODO: check thật
        "graphrag_ready": True,  # TODO: check thật
    }
