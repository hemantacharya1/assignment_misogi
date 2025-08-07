# rag_pipeline.py
import os
import base64
from typing import List
from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_core.messages import HumanMessage
from langchain_core.prompts import PromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from unstructured.partition.pdf import partition_pdf
from unstructured.partition.docx import partition_docx
from unstructured.partition.image import partition_image
from unstructured.partition.text import partition_text
from unstructured.documents.elements import Image
from langchain_ollama import ChatOllama
from langchain_ollama import OllamaEmbeddings
load_dotenv()

text_llm = ChatOllama(model="gemma2:2b")
vision_llm = ChatOllama(model="gemma3:4b")
embedding_model = OllamaEmbeddings(model="nomic-embed-text:latest")
DB_SAVE_PATH = "db/faiss_index_multimodal"

PROCESSOR_MAP = {
    ".pdf": partition_pdf,
    ".docx": partition_docx,
    ".txt": partition_text,
    ".jpg": partition_image,
    ".jpeg": partition_image,
    ".png": partition_image,
}


def partition_document(file_path: str):
    _, file_extension = os.path.splitext(file_path)
    file_extension = file_extension.lower()
    processor = PROCESSOR_MAP.get(file_extension)
    print("file extension and processor",processor,file_extension)
    if not processor:
        raise ValueError(f"No processor for file type: {file_extension}")

    if processor == partition_image:
        return processor(file_path)
    elif processor == partition_pdf:
        return processor(file_path, extract_images_in_pdf=True, infer_table_structure=True)
    else:
        return processor(file_path)


def summarize_image(image_data: bytes) -> str:
    prompt = HumanMessage(
        content=[
            {"type": "text", "text": "Describe the image in detail."},
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64.b64encode(image_data).decode()}"}}
        ]
    )
    response = vision_llm.invoke([prompt])
    return response.content


def process_elements_to_documents(elements, file_path: str) -> List[Document]:
    documents = []
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    
    print(elements)
    for i, element in enumerate(elements):
            print("Raw element text",element)
            if isinstance(element, Image):
                print("Image type",element)
                image_path = element.metadata.image_path
                if image_path and os.path.exists(image_path):
                    with open(image_path, "rb") as img_file:
                        image_bytes = img_file.read()
                        summary = summarize_image(image_bytes)
                        metadata = {"source": file_path, "element_index": i, "content_type": "image_summary"}
                        documents.append(Document(page_content=summary, metadata=metadata))
            else:
                print("Text type",element)
                metadata = {"source": file_path, "element_index": i}
                content = element.text.decode() if isinstance(element.text, bytes) else element.text
                chunks = splitter.create_documents([content], metadatas=[metadata])
                documents.extend(chunks)
    return documents


def ingest_file(file_path: str):
    elements = partition_document(file_path)
    print(elements)
    documents = process_elements_to_documents(elements, file_path)
    print(documents)
    db = FAISS.from_documents(documents, embedding_model)
    db.save_local(DB_SAVE_PATH)
    return len(documents)


def load_vector_db():
    return FAISS.load_local(DB_SAVE_PATH, embedding_model, allow_dangerous_deserialization=True)


def ask_question(question: str) -> dict:
    db = load_vector_db()
    relevant_docs = db.similarity_search(question, k=4)
    context = "\n\n".join(doc.page_content for doc in relevant_docs)

    prompt_template = """
    You are a helpful assistant. Use the following context to answer the question:

    Context:
    {context}

    Question: {question}

    Answer:
    """
    prompt = PromptTemplate.from_template(prompt_template)
    response = text_llm.invoke(prompt.format(context=context, question=question))

    return {
        "answer": response.content,
        "sources": [doc.metadata for doc in relevant_docs]
    }
