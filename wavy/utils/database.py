import os

from datetime import datetime
from . import classes
from motor import motor_asyncio


class Database:
    """Class that contains database-related functions."""

    def __init__(self):
        database = self.connect()

        self.client = database[0]
        self.db = database[1]

    @staticmethod
    def connect() -> motor_asyncio.AsyncIOMotorClient:
        """Connects to the db."""
        conn_str = os.environ["DB_CONN_STR"]
        client = motor_asyncio.AsyncIOMotorClient(
            conn_str, serverSelectionTimeoutMS=5000
        )

        db = client.wavy

        return client, db

    async def set_warn(
        self, server_id: int, member_id: int, warn_id: str, reason: str
    ) -> str:
        """Sets a warn for a member."""
        collection = self.db.warns

        document = {
            "server_id": server_id,
            "member_id": member_id,
            "warn_id": warn_id,
            "reason": reason,
        }

        result = await collection.insert_one(document)

        return result.inserted_id

    async def fetch_warns(self, member_id: int) -> list:
        """Fetches all warns for a member."""
        collection = self.db.warns

        cursor = collection.find({"member_id": member_id})

        warns = []

        async for document in cursor:
            warn_class = classes.Warn(
                server_id=document["server_id"],
                member_id=document["member_id"],
                id=document["warn_id"],
                reason=document["reason"],
            )

            warns.append(warn_class)

        return warns

    async def remove_warn(self, server_id: int, warn_id: str) -> bool:
        """Removes a warn."""
        collection = self.db.warns

        result = await collection.delete_one(
            {"server_id": server_id, "warn_id": warn_id}
        )

        return result.deleted_count > 0

    async def set_snipe(
        self,
        server_id: str,
        channel_id: int,
        member_id: int,
        content: str,
        attachments: list,
    ) -> str or None:
        """Sets a snipe."""
        collection = self.db.snipes

        # Delete snipe after 30 minutes.
        await collection.create_index([("createdAt", 1)], expireAfterSeconds=1800)

        old_document = await collection.find_one(
            {"server_id": server_id, "channel_id": channel_id}
        )

        document = {
            "createdAt": datetime.utcnow(),
            "server_id": server_id,
            "channel_id": channel_id,
            "member_id": member_id,
            "content": content,
            "attachments": attachments,
        }

        if old_document:
            await self.db.snipes.update_many(
                {
                    "createdAt": old_document["createdAt"],
                    "member_id": old_document["member_id"],
                    "content": old_document["content"],
                    "attachments": old_document["attachments"],
                },
                {
                    "$set": {
                        "createdAt": datetime.utcnow(),
                        "member_id": member_id,
                        "content": content,
                        "attachments": attachments,
                    }
                },
            )
        else:
            result = await self.db.snipes.insert_one(document)

            return result.inserted_id

    async def get_snipe(self, server_id: int, channel_id: int) -> classes.Snipe or None:
        """Gets a snipe."""
        collection = self.db.snipes

        document = await collection.find_one(
            {"server_id": server_id, "channel_id": channel_id}
        )

        if document:
            snipe_class = classes.Snipe(
                created_at=document["createdAt"],
                server_id=document["server_id"],
                channel_id=document["channel_id"],
                member_id=document["member_id"],
                content=document["content"],
                attachments=document["attachments"],
            )

            return snipe_class
        return
