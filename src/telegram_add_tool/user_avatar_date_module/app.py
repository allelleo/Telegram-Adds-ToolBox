import asyncio
import os
from datetime import datetime

from dotenv import load_dotenv
from telethon import TelegramClient
import httpx

load_dotenv()

API_ID = os.getenv('api_id')
API_HASH = os.getenv('api_hash')
BACKEND_URL = os.getenv('backend_url')

type username = str

async def get_user(session_name: str) -> username:
    """Можно адаптировать под разные аккаунты"""
    return 'allelleo'  # Для примера — одинаковый юзернейм

async def call_backend(year: int, month: int, day: int, hour: int, minute: int, second: int, user: str):
    """Пример вызова backend — подставьте свою логику"""
    print(f"[BACKEND] Calling backend with time: {year}-{month}-{day} {hour}:{minute}:{second}")
    # Пример: отправка через httpx
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{BACKEND_URL}/set-user-first-avatar", json={
            "year": year,
            "month": month,
            "day": day,
            "hour": hour,
            "minute": minute,
            "second": second,
            "user": user
        })
        print(f"[BACKEND] Response: {response.status_code} - {response.text}")

async def worker(session_name: str):
    os.makedirs("downloads", exist_ok=True)
    os.makedirs(f"downloads/{session_name}", exist_ok=True)
    client = TelegramClient(session_name, API_ID, API_HASH)
    await client.start()

    user = await get_user(session_name)
    photos = await client.get_profile_photos(user)

    filepaths = []
    for photo in photos:
        dt = photo.date
        filename = dt.strftime("photo_%Y-%m-%d_%H-%M-%S") + ".jpg"
        filepath = os.path.join("downloads",session_name, filename)

        await client.download_media(photo, file=filepath)
        print(f"[{session_name}] ✅ Скачано: {filepath}")
        filepaths.append(filepath)

    file_times = []
    for path in filepaths:
        name = os.path.basename(path)
        photo_date = name.replace("photo_", "").replace(".jpg", "")
        date_part, time_part = photo_date.split("_")
        year, month, day = map(int, date_part.split("-"))
        hour, minute, second = map(int, time_part.split("-"))

        file_times.append(datetime(year, month, day, hour, minute, second))
        os.remove(path)

    file_times.sort()

    if file_times:
        await call_backend(
            year=file_times[0].year,
            month=file_times[0].month,
            day=file_times[0].day,
            hour=file_times[0].hour,
            minute=file_times[0].minute,
            second=file_times[0].second,
            user=user
        )

async def main():
    # Имена сессий
    sessions = ["user_avatar_1", "user_avatar_2", "user_avatar_3"]
    await asyncio.gather(*(worker(session) for session in sessions))

if __name__ == '__main__':
    asyncio.run(main())
