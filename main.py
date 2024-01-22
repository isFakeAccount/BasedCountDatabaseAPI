from __future__ import annotations

from contextlib import asynccontextmanager
from os import getenv
from typing import AsyncGenerator

from fastapi import FastAPI, Path, Query
from motor.motor_asyncio import (
    AsyncIOMotorClient,
)

from database_query import get_based_count, get_pills, get_based_count_and_pills
from data_models import Pill


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    cluster = AsyncIOMotorClient(getenv("MONGO_PASS"))
    app.state.databased = cluster["dataBased"]
    try:
        yield
    finally:
        cluster.close()


app = FastAPI(lifespan=lifespan)


@app.get("/get_based_count/{user_name}")
async def based_count(user_name: str = Path(..., description="The username for which to retrieve based count.")) -> dict[str, int | str]:
    return await get_based_count(user_name, app.state.databased)


@app.get("/get_pills/{user_name}")
async def pills(
    user_name: str = Path(..., description="The username for which to retrieve pills."),
    limit: int = Query(default=10, description="The maximum number of recent pills to return.", ge=10, le=30),
) -> dict[str, list[Pill] | str]:
    return await get_pills(user_name, limit, app.state.databased)


@app.get("/get_based_count_and_pills/{user_name}")
async def based_count_and_pills(
    user_name: str = Path(..., description="The username for which to retrieve based count and pills."),
    limit: int = Query(default=10, description="The maximum number of recent pills to return.", ge=10, le=30),
) -> dict[str, list[Pill] | int | str]:
    return await get_based_count_and_pills(user_name, limit, app.state.databased)


@app.get("/")
def root() -> str:
    return "Hello from Space! 🚀"
