import asyncio
from openai import AsyncOpenAI
import pandas as pd

from src.config import OPEN_AI_KEY

client = AsyncOpenAI(api_key=OPEN_AI_KEY)

async def get_embedding(text, model="text-embedding-3-large"):
    text = text.replace("\n", " ")
    response = await client.embeddings.create(
        input=[text],
        model=model
    )
    return response.data[0].embedding
