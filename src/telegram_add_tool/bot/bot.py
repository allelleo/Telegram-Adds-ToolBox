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
    user_action = event.new_chat_member.status

    # ✅ Если пользователь вступил (а не вышел)
    if user_action == "member":
        try:
            await bot.send_message(
                chat_id=user.id,
                text=f"Привет, {user.first_name}! 👋 Спасибо за подписку на канал!"
            )
        except Exception as e:
            print(f"❌ Не удалось отправить сообщение пользователю @{user.username}: {e}")

    # 🔄 Логика отправки в backend
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
