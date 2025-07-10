from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.embedder import model  # reuse model here
from services.vector_store import query_vector_db
from services.web_search import search_web
from services.summarizer import summarize_answer

router = APIRouter()

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    answer: str
    sources: list

RELEVANCE_THRESHOLD = 0.75  # cosine similarity cutoff

@router.post("/", response_model=QueryResponse)
async def query(request: QueryRequest):
    query_embedding = model.encode([request.query])[0].tolist()

    results = query_vector_db(query_embedding, top_k=5)
    # results dict contains ids, documents, distances, metadatas
    # If top result score is good enough, synthesize from local chunks
    if results and results['distances'][0][0] < (1 - RELEVANCE_THRESHOLD):
        # synthesize from chunks
        answer = summarize_answer(request.query, results['documents'], results['metadatas'])
        return {"answer": answer, "sources": results['metadatas']}
    
    # Otherwise, fallback to web search
    web_results = search_web(request.query)
    answer = summarize_answer(request.query, web_results['snippets'], web_results['sources'])
    
    return {"answer": answer, "sources": web_results['sources']}
