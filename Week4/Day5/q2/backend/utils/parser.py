import fitz  # PyMuPDF
import docx

def parse_pdf(path: str) -> str:
    text = ""
    doc = fitz.open(path)
    for page in doc:
        text += page.get_text()
    return text

def parse_docx(path: str) -> str:
    doc = docx.Document(path)
    return "\n".join([para.text for para in doc.paragraphs])

def parse_document(path: str) -> str:
    if path.endswith(".pdf"):
        return parse_pdf(path)
    elif path.endswith(".docx"):
        return parse_docx(path)
    else:
        raise ValueError("Unsupported file format")
