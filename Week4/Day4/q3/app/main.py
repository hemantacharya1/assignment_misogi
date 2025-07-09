from fastapi import FastAPI
from app.core.init_db import init_db
from app.api.endpoints import tickets
from app.rag.loader import initialize_vector_store
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Smart Support System")

# Allow your frontend origin
origins = [
    "http://localhost:5173",  # React/Vite default dev server
    # add more origins if needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # or ["*"] to allow all (less secure)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    init_db()
    initialize_vector_store()

app.include_router(tickets.router)
