import os
import asyncio
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.0-flash")

async def generate_with_gemini(prompt):
    try:
        response = model.generate_content(prompt, stream=True)
        for chunk in response:
            if chunk.text:
                await asyncio.sleep(0.01)  # simulate delay for stream effect
                yield chunk.text
    except Exception as e:
        yield f"[Gemini Error]: {str(e)}"
