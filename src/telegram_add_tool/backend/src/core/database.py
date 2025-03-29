# src/oauth/core/database.py

import asyncio
from tortoise import Tortoise
from tortoise.exceptions import DBConnectionError

from src.telegram_add_tool.backend.src.core.logger import logger
from src.telegram_add_tool.backend.src.core.setting import TORTOISE_CONFIG


async def init_db() -> None:
    """
    Инициализирует базу данных с использованием конфигурации Tortoise ORM.
    Если вы используете aerich для миграций, генерацию схем можно отключить.
    """
    try:
        await Tortoise.init(config=TORTOISE_CONFIG)
        # Если не используете миграции через aerich, можно сгенерировать схемы:
        # await Tortoise.generate_schemas()
        logger.info("База данных успешно инициализирована.")
    except DBConnectionError as e:
        logger.error("Ошибка подключения к базе данных:", e)


async def close_db() -> None:
    """
    Закрывает все подключения к базе данных.
    """
    await Tortoise.close_connections()


# Запуск инициализации базы данных для тестирования
if __name__ == "__main__":
    asyncio.run(init_db())
