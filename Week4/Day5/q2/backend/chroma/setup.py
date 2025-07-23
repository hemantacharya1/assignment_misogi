import chromadb
from chromadb.config import Settings
import os

def get_chroma_client():
    persist_directory = os.path.abspath("data/chroma_db")
    client = chromadb.PersistentClient(path=persist_directory)
    return client
