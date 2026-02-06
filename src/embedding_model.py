import logging
import asyncio
from openai import AsyncOpenAI
import pandas as pd

from src.config import OPENAI_KEY

logger = logging.getLogger(__name__)
client = AsyncOpenAI(api_key=OPENAI_KEY)


async def get_embedding(text, model="text-embedding-3-large"):
    logger.debug("get_embedding: model=%s, text_len=%d", model, len(text))
    text = text.replace("\n", " ")
    response = await client.embeddings.create(
        input=[text],
        model=model
    )
    logger.debug("get_embedding: success, embedding_dim=%d", len(response.data[0].embedding))
    return response.data[0].embedding
