# main.py
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
import os
import shutil
from app.rag_pipline import ingest_file, ask_question


os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

app = FastAPI()
UPLOAD_DIR = "data"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/ingest")
async def ingest_document(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    try:
        num_docs = ingest_file(file_path)
        return {"status": "success", "file": file.filename, "documents_indexed": num_docs}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/query")
async def query_document(question: str = Form(...)):
    try:
        result = ask_question(question)
        return result
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
