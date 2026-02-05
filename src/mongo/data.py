from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
import asyncio

import sys
sys.path.append("/Users/ezhilrajselvaraj/Ezhil/ever_quint/perkinswill/hub/marketing_toolkit/")

from src.config import MONGO_DATA_URL

class MongoData():
    def __init__(self):
        self._client = AsyncIOMotorClient(MONGO_DATA_URL)
        self.db = self._client["hub365-data"]
    
    async def get_all_active_users(self, id):
        cursor = self.db[id].find({"isDeleted":False})
        docs = await cursor.to_list(length=None)
        return docs

if __name__ == "__main__":
    obj = MongoData()
    asyncio.run(obj.get_all_active_users("63032385388ad56caccebe80"))
