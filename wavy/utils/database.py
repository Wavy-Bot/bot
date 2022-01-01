import os

from motor import motor_asyncio
from pymongo.errors import ConnectionFailure


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

    async def get_server_info(self):
        try:
            server_info = await self.client.server_info()

            return server_info
        except ConnectionFailure:
            print("Unable to connect to the server.")
