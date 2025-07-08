# backend/api/chat.py
from fastapi import APIRouter
from pydantic import BaseModel
from backend.core.rag import rag_chat

router = APIRouter()

class ChatRequest(BaseModel):
    question: str

@router.post("/chat")
def chat(req: ChatRequest):
    response = rag_chat(req.question)
    return response
