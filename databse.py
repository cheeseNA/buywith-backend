import os

import motor.motor_asyncio
from dotenv import load_dotenv

load_dotenv()

client = motor.motor_asyncio.AsyncIOMotorClient(os.environ.get("MONGO_API_KEY"))

database = client.API_DB
collection_item = database.item
collection_user = database.user
