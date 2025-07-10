from fastapi import FastAPI
from routes import ingest, query

app = FastAPI()

app.include_router(ingest.router, prefix="/api/ingest", tags=["Ingest"])
app.include_router(query.router, prefix="/api/query", tags=["Query"])
