import os
from urllib.parse import unquote

from src.telegram_add_tool.bot.config import TOKEN, BACKEND_URL

from aiogram import Bot, Dispatcher
from aiogram.types import ChatMemberUpdated, File
import httpx

DOWNLOAD_DIR = "downloads"  # Папка для загрузки
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.chat_member()
async def track_new_members(event: ChatMemberUpdated):
    user = event.from_user
    user_photos = await bot.get_user_profile_photos(user_id=user.id)

    for photo in user_photos.photos:
        largest = max(photo, key=lambda x: x.file_size)
        file: File = await bot.get_file(largest.file_id)

        # Получаем путь к файлу
        file_path = file.file_path
        file_bytes = await bot.download_file(file_path)

        # Используем оригинальное имя, которое Telegram использует в file_path
        # Обычно путь такой: photos/file_123.jpg или profile_photos/photo_2025-03-28_12-49-19.jpg
        # Забираем только имя файла с расширением
        filename = os.path.basename(unquote(file_path))
        filepath = os.path.join(DOWNLOAD_DIR, filename)

        with open(filepath, "wb") as f:
            f.write(file_bytes.read())

        print(f"Сохранено фото: {filepath}")

    # Остальной код, отправка в backend
    user_action = event.new_chat_member.status
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{BACKEND_URL}/api/v1/user/new_action",
            json={
                "telegram_id": user.id,
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "is_bot": user.is_bot,
                "is_premium": user.is_premium,
                "action": "enter" if user_action == "member" else "leave",
                "channel_id": event.chat.id,
                "link": (
                    {
                        "link": event.invite_link.invite_link,
                        "creator_id": event.invite_link.creator.id,
                        "creator_username": event.invite_link.creator.username,
                        "creator_first_name": event.invite_link.creator.first_name,
                        "creator_last_name": event.invite_link.creator.last_name,
                        "creator_is_bot": event.invite_link.creator.is_bot,
                        "creator_is_premium": event.invite_link.creator.is_premium,
                    }
                    if event.invite_link
                    else None
                ),
            },
        )
        print(response.status_code)
        print(response.text)

    print(
        f"User: {"@" + user.username if user.username else user.first_name + " " + user.last_name} : {user_action} : {event.invite_link}"
    )
