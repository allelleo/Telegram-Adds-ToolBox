# src/oauth/apps/__init__.py

from fastapi import APIRouter

from src.telegram_add_tool.backend.src.apps.user.api import user_api

api = APIRouter(prefix="/api", tags=["api"])
api.include_router(user_api)
