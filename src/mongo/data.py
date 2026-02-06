import logging
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
import asyncio

from src.config import MONGO_DATA_URL

logger = logging.getLogger(__name__)


class MongoData():
    def __init__(self):
        self._client = AsyncIOMotorClient(MONGO_DATA_URL)
        self.db = self._client["hub365-data"]
        logger.info("MongoData initialized: db=hub365-data")

    async def get_all_active_users(self, id):
        logger.info("get_all_active_users: collection_id=%s", id)
        cursor = self.db[id].find({"isDeleted": False})
        docs = await cursor.to_list(length=None)
        logger.info("get_all_active_users: collection_id=%s, returned %d docs", id, len(docs))
        return docs

if __name__ == "__main__":
    obj = MongoData()
    asyncio.run(obj.get_all_active_users("63032385388ad56caccebe80"))
