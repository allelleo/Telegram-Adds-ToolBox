# Используем официальный образ Python
FROM python:3.12-slim

# Устанавливаем зависимости
RUN apt-get update && apt-get install -y build-essential

# Устанавливаем Poetry
RUN pip install poetry

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы проекта
COPY pyproject.toml poetry.lock ./
COPY src ./src
COPY bot.py ./
COPY migrations ./migrations
COPY manage.py ./
COPY .env ./

# Устанавливаем зависимости проекта
RUN poetry config virtualenvs.create false \
 && poetry install --no-root --no-interaction --no-ansi

# Копируем всё остальное (например, сессии, если нужно)
COPY sessions ./sessions
COPY downloads ./downloads
COPY logs ./logs

CMD ["bash"]
