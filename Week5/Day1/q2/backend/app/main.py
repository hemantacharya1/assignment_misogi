from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from app.models.ollama_wrapper import generate_with_ollama
from app.models.gemini_wrapper import generate_with_gemini
from app.utils.classifier import classify_intent
from app.utils.rag import ingest_documents
from app.utils.rag import retrieve_context
from app.utils.rag import answer_query
app = FastAPI()

ingest_documents()

class PromptRequest(BaseModel):
    prompt: str

class QueryRequest(BaseModel):
    intent: str
    question: str

class AskRequest(BaseModel):
    query: str

@app.post("/ask")
def ask(request: AskRequest):
    return answer_query(request.query)


@app.post("/generate")
async def generate_endpoint(body: PromptRequest):
    prompt = body.prompt

    async def stream_response():
        try:
            async for chunk in generate_with_ollama(prompt):
                yield chunk
        except Exception as e:
            print("[Fallback to Gemini]");
            async for chunk in generate_with_gemini(prompt):
                yield chunk

    return StreamingResponse(stream_response(), media_type="text/plain")

@app.post("/classify")
def classify_route(body: PromptRequest):
    intent, score = classify_intent(body.prompt)
    return {
        "intent": intent,
        "confidence": round(score, 3)
    }

@app.post("/query")
def query_rag(req: QueryRequest):
    try:
        docs = retrieve_context(req.intent, req.question)
        return {"relevant_chunks": docs}
    except Exception as e:
        return {"error": str(e)}