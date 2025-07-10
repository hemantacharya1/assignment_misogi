from fastapi import FastAPI
from routes import upload, query
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI(title="Hybrid RAG Research Assistant")

app.include_router(upload.router, prefix="/upload", tags=["Upload"])
app.include_router(query.router, prefix="/query", tags=["Query"])
