import asyncio
from openai import AsyncOpenAI
import pandas as pd

from src.config import OPENAI_KEY

client = AsyncOpenAI(api_key=OPENAI_KEY)

async def get_embedding(text, model="text-embedding-3-large"):
    text = text.replace("\n", " ")
    response = await client.embeddings.create(
        input=[text],
        model=model
    )
    return response.data[0].embedding
