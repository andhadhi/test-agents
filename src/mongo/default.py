import logging
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
import asyncio

from src.config import MONGO_DEFAULT_URL

logger = logging.getLogger(__name__)


class MongoDefault:
    def __init__(self):
        self._client = AsyncIOMotorClient(MONGO_DEFAULT_URL)
        self.db = self._client["hub365-os"]
        self.user_collection = self.db["users"]
        logger.info("MongoDefault initialized: db=hub365-os, collection=users")

    async def get_user_details(self, id):
        logger.debug("get_user_details: user_id=%s", id)
        docs = await self.user_collection.find_one(
            {"_id": ObjectId(id)}
        )
        if docs is None:
            logger.warning("get_user_details: user_id=%s not found", id)
        return docs

if __name__=="__main__":
    obj = MongoDefault()
    asyncio.run(obj.get_user_details("5fb29a8e8532ea44674f38a1"))