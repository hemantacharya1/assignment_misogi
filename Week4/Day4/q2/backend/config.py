# backend/config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    USE_FAST_WHISPER = os.getenv("USE_FAST_WHISPER", "True") == "True"
    CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH", "./data/db")

settings = Settings()
