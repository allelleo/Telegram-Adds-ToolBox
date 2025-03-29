# src/oauth/core/settings.py

import os

APP_NAME = "Telegram Tool"
APP_DESCRIPTION = "Telegram Tool"
APP_VERSION = "1.0.0"

TORTOISE_CONFIG = {
    "connections": {
        "default": {
            "engine": "tortoise.backends.asyncpg",
            "credentials": {
                "host": os.getenv("db_host", "localhost"),
                "port": os.getenv("db_port", 5432),
                "user": os.getenv("db_user", "root"),
                "password": os.getenv("db_password", "<PASSWORD>"),
                "database": os.getenv("db_name", "main"),
            },
        }
    },
    "apps": {
        "models": {
            "models": [
                # "src.oauth.apps.post.models" - пример добавления моделей
                "src.telegram_add_tool.backend.src.apps.user.models",
                "aerich.models",  # aerich миграции
            ],
            "default_connection": "default",
        }
    },
}

ENABLE_TIME_MIDDLEWARE = True
ENABLE_CORS_MIDDLEWARE = True
CORS_MIDDLEWARE_ALLOW_ORIGINS = ["*"]
CORS_MIDDLEWARE_ALLOW_HEADERS = ["*"]
