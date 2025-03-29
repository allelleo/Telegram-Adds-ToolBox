# src/oauth/core/lifespan.py

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI

from src.telegram_add_tool.backend.src.core.database import init_db, close_db


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    await init_db()
    yield
    await close_db()
