import os
from datetime import datetime, timedelta

import httpx
from telethon.sync import TelegramClient
from telethon.tl.types import (
    UserStatusOnline,
    UserStatusOffline,
    UserStatusRecently,
    UserStatusLastWeek,
    UserStatusLastMonth,
)
from dotenv import load_dotenv

load_dotenv()

# 👉 Введи свои значения
token = os.getenv("bot_token")

API_ID = os.getenv("api_id")
API_HASH = os.getenv("api_hash")
BACKEND_URL = os.getenv("backend_url")
session_name = "sessions/online_checker"

# 👤 Список Telegram ID


async def get_users(limit, offset):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BACKEND_URL}/api/v1/user/get-user-with-pagination-with-username?limit={limit}&offset={offset}"
        )
        print(response.json())
    return response.json()


async def send_status(data):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{BACKEND_URL}/api/v1/user/set-user-online-status", json={"data": data}
        )
        print(response.json())


async def process_status(status):
    now = datetime.now()
    week = now - timedelta(days=7)
    month = now - timedelta(days=30)
    processed = []
    for item in status:

        if isinstance(item["status"], datetime):
            processed.append(
                {
                    "telegram_id": item["telegram_id"],
                    "date": {
                        "year": item["status"].year,
                        "month": item["status"].month,
                        "day": item["status"].day,
                        "hour": item["status"].hour,
                        "minute": item["status"].minute,
                        "second": item["status"].second,
                    },
                }
            )
        if item["status"] is True:
            processed.append(
                {
                    "telegram_id": item["telegram_id"],
                    "date": {
                        "year": now.year,
                        "month": now.month,
                        "day": now.day,
                        "hour": now.hour,
                        "minute": now.minute,
                        "second": now.second,
                    },
                }
            )
        elif item["status"] == "week":
            processed.append(
                {
                    "telegram_id": item["telegram_id"],
                    "date": {
                        "year": week.year,
                        "month": week.month,
                        "day": week.day,
                        "hour": week.hour,
                        "minute": week.minute,
                        "second": week.second,
                    },
                }
            )
        elif item["status"] == "month":
            processed.append(
                {
                    "telegram_id": item["telegram_id"],
                    "date": {
                        "year": month.year,
                        "month": month.month,
                        "day": month.day,
                        "hour": month.hour,
                        "minute": month.minute,
                        "second": month.second,
                    },
                }
            )
        else:
            pass
        print(processed)
        print("Sending data to backend")
        await send_status(processed)


async def check_users_online_status(data):
    satus_data = []
    async with TelegramClient(session_name, API_ID, API_HASH) as client:
        for entity in data:
            try:
                user = await client.get_entity(entity["username"])
                status = user.status

                if isinstance(status, UserStatusOnline):
                    print(f"{user.first_name or 'User'} [{user.id}]: 🟢 Онлайн")
                    satus_data.append(
                        {"telegram_id": entity["telegram_id"], "status": True}
                    )
                elif isinstance(status, UserStatusOffline):
                    clear = str(status.was_online).split("+")[0]
                    first, second = clear.split(" ")
                    year, month, day = first.split("-")
                    hour, minute, second = second.split(":")

                    satus_data.append(
                        {
                            "telegram_id": entity["telegram_id"],
                            "status": datetime(
                                int(year),
                                int(month),
                                int(day),
                                int(hour),
                                int(minute),
                                int(second),
                            ),
                        }
                    )
                    print(
                        f"{user.first_name or 'User'} [{user.id}]: 🔴 Был(а) в сети: {status.was_online}"
                    )
                elif isinstance(status, UserStatusRecently):
                    satus_data.append(
                        {"telegram_id": entity["telegram_id"], "status": False}
                    )
                    print(f"{user.first_name or 'User'} [{user.id}]: 🟡 Был(а) недавно")
                elif isinstance(status, UserStatusLastWeek):
                    satus_data.append(
                        {"telegram_id": entity["telegram_id"], "status": "week"}
                    )
                    print(
                        f"{user.first_name or 'User'} [{user.id}]: 🕒 Был(а) в течение недели"
                    )
                elif isinstance(status, UserStatusLastMonth):
                    satus_data.append(
                        {"telegram_id": entity["telegram_id"], "status": "month"}
                    )
                    print(
                        f"{user.first_name or 'User'} [{user.id}]: 📆 Был(а) в течение месяца"
                    )
                else:
                    satus_data.append(
                        {"telegram_id": entity["telegram_id"], "status": "unknown"}
                    )
                    print(
                        f"{user.first_name or 'User'} [{user.id}]: ❔ Статус неизвестен"
                    )
            except Exception as e:
                pass
    print(satus_data)
    print("Processing status")
    await process_status(satus_data)


async def main():
    while True:
        limit = 100
        offset = 0
        data = await get_users(limit, offset)
        while data:
            await check_users_online_status(data)
            offset += 100
            data = await get_users(limit, offset)
        await asyncio.sleep(60 * 60)


import asyncio

asyncio.run(main())
