# src/oauth/core/middleware.py

import time

from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware

from src.telegram_add_tool.backend.src.core.logger import logger


class TimeMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI):
        super().__init__(app)

    async def dispatch(self, request, call_next):
        start_time = time.time()
        response = await call_next(request)
        response.headers["X-Response-Time"] = str(time.time() - start_time)
        logger.info(
            f"Response time: {time.time() - start_time} path {request.url.path}"
        )
        return response
