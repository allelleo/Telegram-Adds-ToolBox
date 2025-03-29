from fastapi import APIRouter

from src.telegram_add_tool.backend.src.apps.user.api.user import main_user_api

user_api = APIRouter(prefix="/v1")
user_api.include_router(main_user_api)
