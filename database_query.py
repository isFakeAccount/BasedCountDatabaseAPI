from __future__ import annotations

import re

from async_lru import alru_cache
from motor.motor_asyncio import AsyncIOMotorCollection, AsyncIOMotorDatabase

from data_models import Pill


@alru_cache(ttl=60, maxsize=256)
async def get_mongo_collection(collection_name: str, databased: AsyncIOMotorDatabase) -> AsyncIOMotorCollection:
    """Returns the user databased from dataBased Cluster from MongoDB

    :returns: Returns a Collection from Mongo DB

    """
    return databased[collection_name]


@alru_cache(ttl=60, maxsize=256)
async def get_based_count(user_name: str, databased: AsyncIOMotorDatabase) -> dict[str, int | str]:
    users_collection = await get_mongo_collection(collection_name="users", databased=databased)
    profile = await users_collection.find_one({"name": re.compile(rf"^{user_name}$", re.I)})

    if profile is not None:
        return {"user_name": user_name, "based_count": profile["count"]}
    else:
        return {"user_name": user_name, "based_count": 0}


@alru_cache(ttl=60, maxsize=128)
async def get_pills(user_name: str, limit: int, databased: AsyncIOMotorDatabase) -> dict[str, list[Pill] | str]:
    users_collection = await get_mongo_collection(collection_name="users", databased=databased)
    profile = await users_collection.find_one({"name": re.compile(rf"^{user_name}$", re.I)})

    if profile is not None:
        pills_data = profile["pills"][-limit:]
        return {"user_name": user_name, "pills": [Pill.from_data(pill=pill) for pill in reversed(pills_data)]}
    else:
        return {"user_name": user_name, "pills": []}


@alru_cache(ttl=60, maxsize=128)
async def get_based_count_and_pills(user_name: str, limit: int, databased: AsyncIOMotorDatabase) -> dict[str, list[Pill] | int | str]:
    users_collection = await get_mongo_collection(collection_name="users", databased=databased)
    profile = await users_collection.find_one({"name": re.compile(rf"^{user_name}$", re.I)})

    if profile is not None:
        pills_data = profile["pills"][-limit:]
        return {"user_name": user_name, "based_count": profile["count"], "pills": [Pill.from_data(pill=pill) for pill in reversed(pills_data)]}
    else:
        return {"user_name": user_name, "based_count": 0, "pills": []}
