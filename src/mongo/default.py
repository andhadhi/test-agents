from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
import asyncio

from src.config import MONGO_DEFAULT_URL

class MongoDefault:
    def __init__(self):
        self._client = AsyncIOMotorClient(MONGO_DEFAULT_URL)
        self.db = self._client["hub365-os"]
        self.user_collection = self.db["users"]

    async def get_user_details(self, id):
        docs = await self.user_collection.find_one(
            {"_id": ObjectId(id)}
        )
        return docs

if __name__=="__main__":
    obj = MongoDefault()
    asyncio.run(obj.get_user_details("5fb29a8e8532ea44674f38a1"))