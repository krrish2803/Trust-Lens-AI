"""
TrustLens AI - Async MongoDB Driver Module
Manages Motor MongoDB connection pool, collections (history, users, reports), and index creation.
Provides in-memory fallback if MongoDB instance is unreachable.
"""

import logging
from motor.motor_asyncio import AsyncIOMotorClient
from backend.config import settings

logger = logging.getLogger("trustlens.db")


class MongoDBManager:
    def __init__(self):
        self.client: AsyncIOMotorClient = None
        self.db = None
        self.is_connected: bool = False
        self._memory_history = []
        self._memory_users = []

    async def connect(self):
        try:
            self.client = AsyncIOMotorClient(
                settings.MONGODB_URI,
                serverSelectionTimeoutMS=2000,
            )
            await self.client.admin.command('ping')
            self.db = self.client[settings.MONGODB_DB_NAME]
            self.is_connected = True
            logger.info("Successfully connected to MongoDB")

            await self.db.history.create_index("id", unique=True)
            await self.db.history.create_index("created_at")
            await self.db.history.create_index("scan_type")
            await self.db.reports.create_index("scan_id")

        except Exception as e:
            self.is_connected = False
            logger.warning("MongoDB connection failed: %s. Operating with in-memory storage fallback.", type(e).__name__)

    async def close(self):
        if self.client:
            self.client.close()
            logger.info("MongoDB client connection closed.")


db_manager = MongoDBManager()
