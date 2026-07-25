"""
TrustLens AI - Scan History Data Access Layer
Handles reading and writing scan history records to MongoDB with in-memory fallback.
"""

import uuid
from typing import List, Dict, Any, Optional
from datetime import datetime
from backend.database.mongodb import db_manager


class HistoryRepository:
    def __init__(self):
        pass

    async def save_scan(self, scan_data: Dict[str, Any]) -> str:
        """
        Saves scan result to MongoDB history collection or memory cache.
        """
        scan_id = scan_data.get("id") or str(uuid.uuid4())
        scan_data["id"] = scan_id
        if "created_at" not in scan_data:
            scan_data["created_at"] = datetime.utcnow().isoformat()

        if db_manager.is_connected and db_manager.db is not None:
            try:
                await db_manager.db.history.insert_one(dict(scan_data))
            except Exception as e:
                db_manager._memory_history.insert(0, scan_data)
        else:
            db_manager._memory_history.insert(0, scan_data)
            # Limit in-memory history size
            if len(db_manager._memory_history) > 100:
                db_manager._memory_history.pop()

        return scan_id

    async def get_history(self, limit: int = 50, skip: int = 0) -> List[Dict[str, Any]]:
        """
        Retrieves scan history items.
        """
        if db_manager.is_connected and db_manager.db is not None:
            try:
                cursor = db_manager.db.history.find(
                    {}, {"_id": 0}
                ).sort("created_at", -1).skip(skip).limit(limit)
                items = await cursor.to_list(length=limit)
                return items
            except Exception:
                pass

        return db_manager._memory_history[skip : skip + limit]

    async def get_scan_by_id(self, scan_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieves a single scan result by ID.
        """
        if db_manager.is_connected and db_manager.db is not None:
            try:
                doc = await db_manager.db.history.find_one({"id": scan_id}, {"_id": 0})
                if doc:
                    return doc
            except Exception:
                pass

        for item in db_manager._memory_history:
            if item.get("id") == scan_id:
                return item
        return None


history_repo = HistoryRepository()
