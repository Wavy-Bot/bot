import os
import random

from typing import List, Union, Optional
from datetime import datetime, timedelta
from . import classes
from motor import motor_asyncio


class Database:
    """Class that contains database-related functions."""

    # TODO(Robert): Rewrite this, especially the meme-related functions.

    def __init__(self):
        self.client = self.connect()
        self.db = self.client.wavy

    def __del__(self):
        self.client.close()

    @staticmethod
    def connect() -> motor_asyncio.AsyncIOMotorClient:
        """Connects to the db.

        :rtype:  motor_asyncio.AsyncIOMotorClient
        """
        conn_str = os.environ["DB_CONN_STR"]
        client = motor_asyncio.AsyncIOMotorClient(
            conn_str, serverSelectionTimeoutMS=5000
        )

        return client

    async def set_warn(
        self, server_id: int, member_id: int, warn_id: str, reason: str
    ) -> None:
        """Sets a warn for a member.

        :param int server_id: The ID of the server.
        :param int member_id: The ID of the member.
        :param str warn_id: The ID of the warn.
        :param str reason: The reason for the warn.

        :rtype:  None
        """
        collection = self.db.warns

        document = {
            "server_id": server_id,
            "member_id": member_id,
            "warn_id": warn_id,
            "reason": reason,
        }

        await collection.insert_one(document)

    async def fetch_warns(self, member_id: int) -> List[classes.Warn]:
        """Fetches all warns for a member.

        :param int member_id: The ID of the member.

        :return:      A list of classes.Warn
        :rtype:  List[Warn]
        """
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
        """Removes a warn.

        :param int server_id: The ID of the server.
        :param str warn_id: The ID of the warn.

        :return: Wether or not the warn could be removed.
        :rtype:  bool
        """
        collection = self.db.warns

        result = await collection.delete_one(
            {"server_id": server_id, "warn_id": warn_id}
        )

        return result.deleted_count > 0

    async def fetch_memes(self) -> dict:
        """Fetches all memes."""
        collection = self.db.memes

        document = await collection.find_one()

        return document

    async def fetch_meme(self) -> Optional[classes.RedditPost]:
        """Fetches all memes.

        :return: A random meme.
        :rtype:  dict or None
        """
        collection = self.db.memes

        document = await collection.find_one()

        if document:
            memes = document.get("memes", [])

            if memes:
                meme = random.choice(memes)

                meme_class = classes.RedditPost(
                    subreddit=meme["subreddit"],
                    title=meme["title"],
                    over_18=meme["over_18"],
                    url=meme["url"],
                    image=meme["image"],
                    ups=meme["ups"],
                    comments=meme["comments"],
                )

                return meme_class
        return

    async def set_memes(self, memes: List[dict]) -> Optional[int]:
        """Adds memes to the database.

        :param list memes: A list of RedditPost objects.

        :return: The memes that were added.
        :rtype:  int or None
        """
        collection = self.db.memes

        # Delete memes after 15 minutes.
        await collection.create_index([("createdAt", 1)], expireAfterSeconds=900)

        old_document = await self.fetch_memes()

        document = {"createdAt": datetime.utcnow(), "memes": memes}

        if old_document:
            # Delete memes older than 1 hour.
            if not old_document["createdAt"] + timedelta(hours=1) >= datetime.utcnow():
                memes = memes + old_document["memes"]

                # Remove duplicates.
                memes = [dict(t) for t in {tuple(d.items()) for d in memes}]

                await collection.update_many(
                    {
                        "createdAt": old_document["createdAt"],
                        "memes": old_document["memes"],
                    },
                    {
                        "$set": {
                            "createdAt": datetime.utcnow(),
                            "memes": memes,
                        }
                    },
                )
            else:
                await collection.delete_one({"createdAt": old_document["createdAt"]})

                await collection.insert_one(document)
            return
        result = await collection.insert_one(document)

        return result.inserted_id

    async def update_command_stats(self, command: str) -> None:
        """Updates the command stats.

        :param str command: The command to update.

        :rtype:  None
        """
        collection = self.db.command_stats

        # Get the current stats of the command, or create a new one if it doesn't exist.
        # Then, update or insert the stats.
        document = await collection.find_one({"command": command})

        if document:
            await collection.update_one(
                {"command": command},
                {"$inc": {"count": 1}},
            )
        else:
            await collection.insert_one({"command": command, "count": 1})
