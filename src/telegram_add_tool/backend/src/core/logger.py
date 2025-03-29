# src/oauth/core/logger.py

import logging
import logging.handlers
import os

# Папка для логов
LOG_DIR = "logs"
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# Создаем логгер с именем 'backend'
logger = logging.getLogger("backend")
logger.setLevel(logging.DEBUG)

# Формат логов
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# Обработчик для вывода в консоль
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# Обработчик для записи логов в файл с ротацией
file_handler = logging.handlers.RotatingFileHandler(
    os.path.join(LOG_DIR, "app.log"),
    maxBytes=5 * 1024 * 1024,
    backupCount=3,
    encoding="utf-8",
)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Настройка логирования SQL-запросов от Tortoise ORM
tortoise_logger = logging.getLogger("tortoise")
tortoise_logger.setLevel(logging.DEBUG)
tortoise_logger.addHandler(console_handler)
tortoise_logger.addHandler(file_handler)

# Пример использования логгера
if __name__ == "__main__":
    logger.debug("Сообщение DEBUG")
    logger.info("Сообщение INFO")
    logger.warning("Сообщение WARNING")
    logger.error("Сообщение ERROR")
    logger.critical("Сообщение CRITICAL")
    tortoise_logger.debug("Пример SQL-запроса")
