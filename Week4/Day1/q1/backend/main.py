from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from llm_utils import ask_gemini
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QuestionRequest(BaseModel):
    question: str

@app.post("/ask")
async def ask_question(payload: QuestionRequest):
    question = payload.question.strip()
    if not question:
        raise HTTPException(status_code=400, detail="Question cannot be empty.")
    answer = ask_gemini(question)
    return {"answer": answer}
