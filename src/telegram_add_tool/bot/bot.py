import os
from aiogram.filters import Command, CommandObject

from src.telegram_add_tool.bot.adapter import (
    check_user_access,
    get_channels_adapter,
    get_channel_info,
    get_link_active_adapter,
)
from src.telegram_add_tool.bot.config import TOKEN, BACKEND_URL

from aiogram import Bot, Dispatcher, F
from aiogram.types import (
    ChatMemberUpdated,
    File,
    Message,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    CallbackQuery,
)
import httpx

import re


def escape_markdown(text: str) -> str:
    return re.sub(r"([_*`\[\]])", r"\\\1", text)


DOWNLOAD_DIR = "downloads"  # Папка для загрузки
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.chat_member()
async def track_new_members(event: ChatMemberUpdated):
    user = event.from_user
    user_action = event.new_chat_member.status

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


@dp.message(Command("panel"))
async def panel(message: Message):
    user_telegram_id = message.from_user.id
    result = await check_user_access(user_id=user_telegram_id)
    if isinstance(result, bool):
        await message.reply("No access")

    if isinstance(result, tuple):
        await bot.send_message(
            chat_id=-4780015746,
            text=f"""[bot] Ошибка проверки доступа\ncode: {result[0]}\ntext: {result[1]}\n@allelleo""",
        )
        return

    if isinstance(result, str):
        await message.reply(
            f"Hello, {result}!",
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text="Channels", callback_data="get_channels"
                        ),
                    ],
                ]
            ),
        )


@dp.callback_query(F.data == "get_channels")
async def get_channels(callback: CallbackQuery):
    user_telegram_id = callback.from_user.id
    result = await check_user_access(user_id=user_telegram_id)
    if isinstance(result, bool):
        await callback.message.answer("No access")
        return
    if isinstance(result, tuple):
        await bot.send_message(
            chat_id=-4780015746,
            text=f"""[bot] Ошибка проверки доступа\ncode: {result[0]}\ntext: {result[1]}\n@allelleo""",
        )
        return

    channels = await get_channels_adapter()
    if len(channels) == 0:
        await callback.message.answer("No channels")
        return

    msg = """Вот список всех каналов:\n\n"""
    for channel in channels:
        msg += f"[{channel['id']}] : {channel['title']}\n"
    msg += "\n\nВернуться обратно - /panel"
    await callback.message.edit_text(msg)


@dp.message(Command("channel"))
async def get_channel(message: Message, command: CommandObject):
    user_telegram_id = message.from_user.id
    result = await check_user_access(user_id=user_telegram_id)
    if isinstance(result, bool):
        await message.reply("No access")

    if isinstance(result, tuple):
        await bot.send_message(
            chat_id=-4780015746,
            text=f"""[bot] Ошибка проверки доступа\ncode: {result[0]}\ntext: {result[1]}\n@allelleo""",
        )
        return

    channel = await get_channel_info(int(command.args))
    msg = f"Канал: {channel['channel']['title']}\nID: {channel['channel']['channel_id']}\n\nСсылки: {len(channel['links'])}\n\nСписок ссылок:\n"
    for link in channel["links"]:
        msg += f"[{link['id']}] : {link['link'][0:25]}\n"
    msg += f"\n\nСуммарно действий: {channel['actions']}\nОтследили юзеров: {channel['users']}"

    await message.reply(msg)


@dp.message(Command("channel_users"))
async def get_channel_users(message: Message, command: CommandObject):
    user_telegram_id = message.from_user.id
    result = await check_user_access(user_id=user_telegram_id)
    if isinstance(result, bool):
        await message.reply("No access")

    if isinstance(result, tuple):
        await bot.send_message(
            chat_id=-4780015746,
            text=f"""[bot] Ошибка проверки доступа\ncode: {result[0]}\ntext: {result[1]}\n@allelleo""",
        )
        return


@dp.message(Command("link_active"))
async def get_link_active(message: Message, command: CommandObject):
    user_telegram_id = message.from_user.id
    result = await check_user_access(user_id=user_telegram_id)
    if isinstance(result, bool):
        await message.reply("No access")

    if isinstance(result, tuple):
        await bot.send_message(
            chat_id=-4780015746,
            text=f"""[bot] Ошибка проверки доступа\ncode: {result[0]}\ntext: {result[1]}\n@allelleo""",
        )
        return

    res = await get_link_active_adapter(int(command.args))
    sections_order = [
        "Были в сети",
        "Дата регистрации",
        "Дата постановки аватарки",
    ]

    categories_order = [
        "недавно",
        "6-12 часов назад",
        "13-24 часа назад",
        "на этой неделе",
        "в этом месяце",
        "давно",
        "отсутствует",
        "день",
        "до недели",
        "до месяца",
        "до 3-х месяцев",
        "до полугода",
        "Больше года",
        "Больше 3-ех лет",
    ]

    lines = []

    for section in sections_order:
        lines.append(f"*{section}:*")
        data = res.get(section, {})
        for category in categories_order:
            if category in data:
                value = data[category]
                lines.append(f" • *{category}*: `{value}`")
        lines.append("")  # пустая строка между секциями
    res1 = "\n".join(lines)
    title = escape_markdown(res["channel"]["title"])
    link = escape_markdown(res["channel"]["link"][0:25])

    res2 = (
        f"""Канал: {title}\nСсылка: {link}\n\nПользователи: {res['total']}\nПремиум: {res['is_prem']}\n\n"""
        + res1
    )
    await message.reply(res2, parse_mode="Markdown")
