import os

from bson import ObjectId
import motor.motor_asyncio
from dotenv import load_dotenv

load_dotenv()

client = motor.motor_asyncio.AsyncIOMotorClient(os.environ.get("MONGO_API_KEY"))

database = client.API_DB
collection_item = database.item
collection_user = database.user


def id_serializer(data: dict) -> dict:
    object_id = str(data.pop("_id"))
    data.update({"id": object_id})
    return data


async def db_create_item(data: dict) -> dict | bool:
    item = await collection_item.insert_one(data)
    new_item = await collection_item.find_one({"_id": item.inserted_id})
    if new_item:
        return id_serializer(new_item)
    return False


async def db_get_items(skip: int, limit: int) -> list:
    items = []
    for item in await collection_item.find().skip(skip).limit(limit).to_list(limit):
        items.append(id_serializer(item))
    return items


async def db_get_single_item(id: str) -> dict | bool:
    item = await collection_item.find_one({"_id": ObjectId(id)})
    if item:
        return id_serializer(item)
    return False
