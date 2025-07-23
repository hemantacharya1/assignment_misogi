from fastapi import FastAPI, UploadFile, File
from utils.file_utils import save_upload_file
from utils.parser import parse_document
from utils.chunker import chunk_text
from embeddings.encoder import get_embeddings
from chroma.ingest import store_chunks

app = FastAPI()

@app.post("/upload/")
async def upload_document(file: UploadFile = File(...)):
    if not file.filename.endswith((".pdf", ".docx")):
        return {"error": "Only PDF and DOCX files are supported."}
    
    saved_path = await save_upload_file(file)
    parsed_text = parse_document(saved_path)
    chunks = chunk_text(parsed_text)

    metadata = {
        "filename": file.filename,
        "source": "upload"
    }

    store_chunks(chunks, metadata)

    return {
        "filename": file.filename,
        "total_chunks": len(chunks),
        "preview": chunks[:3]
    }