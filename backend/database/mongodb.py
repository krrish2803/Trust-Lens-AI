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
        # In-memory storage fallback if MongoDB is not running
        self._memory_history = []

    async def connect(self):
        """
        Connects to MongoDB and initializes collections.
        """
        try:
            self.client = AsyncIOMotorClient(
                settings.MONGODB_URI,
                serverSelectionTimeoutMS=2000
            )
            # Test connection
            await self.client.admin.command('ping')
            self.db = self.client[settings.MONGODB_DB_NAME]
            self.is_connected = True
            logger.info(f"Successfully connected to MongoDB at {settings.MONGODB_URI}")

            # Ensure indexes
            await self.db.history.create_index("created_at")
            await self.db.history.create_index("scan_type")
            await self.db.reports.create_index("scan_id")

        except Exception as e:
            self.is_connected = False
            logger.warning(f"MongoDB connection failed: {e}. Operating with in-memory storage fallback.")

    async def close(self):
        if self.client:
            self.client.close()
            logger.info("MongoDB client connection closed.")


db_manager = MongoDBManager()
