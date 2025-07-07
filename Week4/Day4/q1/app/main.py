from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from app.ingestion import process_and_store_document
from fastapi.middleware.cors import CORSMiddleware
from app.query import query_hr_docs

app = FastAPI()

origins = [
    "http://localhost:5173",  # Your React app URL (adjust if different)
    "http://localhost:3000",  # Optional, if you also test on this port
    # You can add more URLs or use "*" for all (not recommended for production)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows requests from these origins
    allow_credentials=True,
    allow_methods=["*"],    # Allow all HTTP methods
    allow_headers=["*"],    # Allow all headers
)

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    content = await file.read()
    result = process_and_store_document(file.filename, content)
    return {"status": "uploaded", "chunks_stored": result}

class QueryRequest(BaseModel):
    query: str

@app.post("/query/")
async def query_docs(request: QueryRequest):
    result = query_hr_docs(request.query)
    return {"answer": result}
