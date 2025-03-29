# src/app.py

from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.telegram_add_tool.backend.src.apps import api
from src.telegram_add_tool.backend.src.core.lifespan import lifespan
from src.telegram_add_tool.backend.src.core.logger import logger
from src.telegram_add_tool.backend.src.core.middleware import TimeMiddleware
from src.telegram_add_tool.backend.src.core.setting import (
    APP_NAME,
    APP_DESCRIPTION,
    APP_VERSION,
    ENABLE_TIME_MIDDLEWARE,
    ENABLE_CORS_MIDDLEWARE,
    CORS_MIDDLEWARE_ALLOW_ORIGINS,
    CORS_MIDDLEWARE_ALLOW_HEADERS,
)

logger.info("Creating app")

app = FastAPI(
    title=APP_NAME, description=APP_DESCRIPTION, version=APP_VERSION, lifespan=lifespan
)

app.include_router(api)
if ENABLE_TIME_MIDDLEWARE:
    app.add_middleware(TimeMiddleware)

if ENABLE_CORS_MIDDLEWARE:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=CORS_MIDDLEWARE_ALLOW_ORIGINS,
        allow_headers=CORS_MIDDLEWARE_ALLOW_HEADERS,
    )
