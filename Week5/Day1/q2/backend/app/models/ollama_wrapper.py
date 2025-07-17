import aiohttp
import json

async def generate_with_ollama(prompt):
    async with aiohttp.ClientSession() as session:
        async with session.post(
            "http://localhost:11434/api/generate",
            json={"model": "qwen3:0.6b", "prompt": prompt, "stream": True}
        ) as resp:
            async for line in resp.content:
                try:
                    data = json.loads(line.decode("utf-8").strip())
                    yield data["response"]
                except Exception:
                    continue
