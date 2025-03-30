import asyncio
import os

from aiogram import Bot
from dotenv import load_dotenv
from telethon import TelegramClient, events
import httpx

load_dotenv()
API_ID = os.getenv("api_id")
API_HASH = os.getenv("api_hash")
BACKEND_URL = os.getenv("backend_url")
token = os.getenv("bot_token")

BOT_USERNAME = os.getenv('check_reg_date')

type t_user_id = int


async def get_user() -> t_user_id:

    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BACKEND_URL}/api/v1/user/get-user-for-check-registration-date")
    if response.status_code == 200:
        print(response.json())
        return int(response.json()["user_id"])
    elif response.status_code == 404:
        await asyncio.sleep(10)
        return await get_user()
    else:
        bot = Bot(token=token)
        await bot.send_message(chat_id=-4780015746,
                               text=f"Ошибка получения user_id\nstatus: {response.status_code}\ntext: {response.text}\n@allelleo")
        await asyncio.sleep(5)
        return await get_user()


async def call_backend(user_id: int, response_text: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{BACKEND_URL}/api/v1/user/set-user-registration-date",
            json={"user_id": user_id, "message": response_text}
        )
        print(f"[BACKEND] Ответ: {response.status_code} - {response.text}")


async def worker(session_name: str):
    client = TelegramClient(session_name, API_ID, API_HASH)
    await client.start()

    user_id = await get_user()
    print(f"[{session_name}] Получен user_id: {user_id}")

    # Отправляем сообщение боту
    bot_entity = await client.get_entity(BOT_USERNAME)
    await client.send_message(bot_entity, str(user_id))
    print(f"[{session_name}] ⏳ Отправлен запрос боту {BOT_USERNAME}")

    # Ждём ответа от бота
    @client.on(events.NewMessage(from_users=bot_entity))
    async def handler(event):
        message = event.message.message
        print(f"[{session_name}] 📩 Ответ от бота: {message}")

        # Отправка на backend
        await call_backend(user_id, message)

        # Завершаем обработку и отключаемся
        await client.disconnect()

    # Ждём события
    await client.run_until_disconnected()


async def main():
    while True:
        await worker("regdate_session")


if __name__ == "__main__":
    asyncio.run(main())
