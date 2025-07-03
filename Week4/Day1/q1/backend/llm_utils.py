import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")

def ask_gemini(question: str) -> str:
    prompt = (
        "You are a helpful technical assistant specializing in the Model Context Protocol (MCP) for AI systems. "
        "Answer the following developer question using up-to-date and you can use these websites to scrap and get data (https://docs.anthropic.com/en/docs/mcp, https://modelcontextprotocol.io/introduction) \n\n"
        f"Question: {question}"
    )
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error contacting Gemini API: {str(e)}"
