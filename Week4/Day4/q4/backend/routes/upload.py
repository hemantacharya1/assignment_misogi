from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from services.pdf_extractor import extract_text_from_pdf
from services.chunker import chunk_text
from services.embedder import embed_chunks
from services.vector_store import add_chunks_to_vector_db

router = APIRouter()

@router.post("/")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    
    contents = await file.read()

    # Extract text from PDF
    text = extract_text_from_pdf(contents)

    # Chunk text semantically
    chunks = chunk_text(text)

    # Embed chunks
    embeddings = embed_chunks(chunks)

    # Add to vector DB (Chroma)
    add_chunks_to_vector_db(chunks, embeddings, source=file.filename)

    return JSONResponse(content={"message": f"Processed {len(chunks)} chunks from {file.filename}"})
