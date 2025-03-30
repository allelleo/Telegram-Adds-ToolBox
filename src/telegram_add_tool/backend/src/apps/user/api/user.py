import os
from datetime import datetime, timedelta

from aiogram import Bot
from fastapi import APIRouter, Request
from starlette.responses import JSONResponse
from tortoise.transactions import in_transaction

from src.telegram_add_tool.backend.src.apps.user.metrics import (
    get_user_metrics,
    get_users_with_link_and_enter_action,
)
from src.telegram_add_tool.backend.src.apps.user.models import (
    UserOrm,
    UserActionHistoryOrm,
    InviteLinksOrm,
    ChannelsOrm,
    BotUserAccessOrm,
    UserActivityStatusOrm,
)
from src.telegram_add_tool.backend.src.apps.user.schemas import (
    NewActionDto,
    SetUserFirstAvatarDto,
    SetUserRegistrationDto,
    UserListStatusDto,
)

main_user_api = APIRouter(prefix="/user")
token = os.getenv("bot_token")


@main_user_api.get("/")
async def index():
    return {"message": "Hello World"}


@main_user_api.post("/new_action")
async def new_action(request: Request, data: NewActionDto):
    channel = await ChannelsOrm.get_or_none(channel_id=data.channel_id)
    if channel is None:
        raise

    is_new_user = None
    is_invite_link = None

    if not data.link is None:
        invite_link = await InviteLinksOrm.get_or_none(link=data.link.link)
        if invite_link is None:
            invite_link = await InviteLinksOrm.create(
                link=data.link.link,
                creator_id=data.link.creator_id,
                creator_username=data.link.creator_username,
                creator_first_name=data.link.creator_first_name,
                creator_last_name=data.link.creator_last_name,
                creator_is_bot=data.link.creator_is_bot,
                creator_is_premium=True if data.link.creator_is_premium else False,
                channel=channel,
            )

        is_invite_link = True
    else:
        is_invite_link = False

    user = await UserOrm.get_or_none(telegram_id=data.telegram_id)
    if user is None:
        user = await UserOrm.create(
            telegram_id=data.telegram_id,
            username=data.username,
            first_name=data.first_name,
            last_name=data.last_name,
            is_bot=data.is_bot,
            is_premium=True if data.is_premium else False,
        )
        is_new_user = True
    else:
        is_new_user = False

    if data.action == "enter":
        actions_count = await UserActionHistoryOrm.filter(
            user=user, channel=channel
        ).count()

        if actions_count > 0:
            message = f"""Пользователь повторно присоединился\n\nКанал: {channel.title} | {channel.channel_id}\nИмя: {user.first_name if user.first_name else "Не указано"}\nФамилия: {user.last_name if user.last_name else "Не указано"}\nЮзернейм: {'@' + user.username if user.username else "Не указано"}\nID: {user.telegram_id}\n\n"""
            first_link = (
                await user.used_links.filter(channel=channel)
                .order_by("created_at")
                .first()
            )
            message += f"Изначальная ссылка: {first_link.link[0:25]}\n"
            if is_invite_link:
                message += f"Новая ссылка: {invite_link.link[0:25]}\n"
            first_enter = (
                await UserActionHistoryOrm.filter(
                    user=user, channel=channel, action="enter"
                )
                .order_by("created_at")
                .first()
            )
            message += (
                f"Время первого захода: {(str(first_enter.created_at)).split('.')[0]}"
            )

            print(message)
            bot = Bot(token=token)
            await bot.send_message(chat_id=-4780015746, text=message)
            await bot.close()

        if is_invite_link:
            await user.used_links.add(invite_link)
            await user.save()

        await UserActionHistoryOrm.create(user=user, channel=channel, action="enter")
        await user.save()
    else:
        await UserActionHistoryOrm.create(user=user, channel=channel, action="leave")
        await user.save()


@main_user_api.post("/set-user-first-avatar")
async def set_user_first_avatar(request: Request, data: SetUserFirstAvatarDto):
    print(data)
    user = await UserOrm.get(username=data.user)
    user.photo_date = datetime(
        year=data.year,
        month=data.month,
        day=data.day,
        hour=data.hour,
        minute=data.minute,
        second=data.second,
    )
    await user.save()
    return JSONResponse(status_code=200, content={})


@main_user_api.get("/get-user-for-check-avatar")
async def get_user_for_check_avatar():
    async with in_transaction() as conn:
        query = """
            SELECT * FROM userorm
            WHERE username IS NOT NULL AND photo_date IS NULL
            ORDER BY RANDOM()
            LIMIT 1
        """
        results = await UserOrm.raw(query)
        if not results:
            return JSONResponse(status_code=404, content={"detail": "No user found"})

        user = results[0]
        return JSONResponse(
            status_code=200,
            content={
                "username": user.username.replace("@", "") if user.username else ""
            },
        )


@main_user_api.post("/set-user-registration-date")
async def set_user_registration_date(request: Request, data: SetUserRegistrationDto):
    user = await UserOrm.get(telegram_id=data.user_id)
    user.registration_message = data.message
    await user.save()
    return JSONResponse(status_code=200, content={})


@main_user_api.get("/get-user-for-check-registration-date")
async def get_user_for_check_registration_date():
    async with in_transaction() as conn:
        query = """
            SELECT * FROM userorm
            WHERE registration_message IS NULL
            ORDER BY RANDOM()
            LIMIT 1
        """
        results = await UserOrm.raw(query)
        if not results:
            return JSONResponse(status_code=404, content={"detail": "No user found"})

        user = results[0]
        return JSONResponse(
            status_code=200,
            content={
                "user_id": user.telegram_id,
            },
        )


@main_user_api.get("/check-user-access")
async def check_user_access(request: Request, telegram_id: int):
    user = await BotUserAccessOrm.get_or_none(telegram_id=telegram_id)
    if user is None:
        return JSONResponse(status_code=404, content={"detail": "No user found"})

    return JSONResponse(
        status_code=200, content={"user_id": user.telegram_id, "name": user.name}
    )


@main_user_api.get("/channels")
async def get_all_channels():
    res = await ChannelsOrm.all()
    data = []
    for channel in res:
        data.append(
            {"id": channel.id, "channel_id": channel.channel_id, "title": channel.title}
        )
    return data


@main_user_api.get("/get-chanel-info")
async def get_all_channel_info(channel_id: int):
    channel = await ChannelsOrm.get(id=channel_id)
    links = await InviteLinksOrm.filter(channel=channel).all()
    actions = await UserActionHistoryOrm.filter(channel=channel).count()
    links_data = []
    links_ids = []
    for link in links:
        links_data.append(
            {
                "id": link.id,
                "link": link.link,
            }
        )
        links_ids.append(link.id)
    users = await UserOrm.filter(used_links__in=links_ids).count()
    return JSONResponse(
        status_code=200,
        content={
            "links": links_data,
            "channel": {
                "id": channel.id,
                "title": channel.title,
                "channel_id": channel.channel_id,
            },
            "actions": actions,
            "users": users,
        },
    )


@main_user_api.get("/pagination")
async def get_all_pagination():
    count = await UserOrm.filter(username__not_isnull=True).count()
    return JSONResponse(status_code=200, content={"count": count})


@main_user_api.get("/get-user-with-pagination-with-username")
async def get_user_with_pagination(request: Request, limit: int, offset: int):
    users = await UserOrm.filter(username__not_isnull=True).offset(offset).limit(limit)
    data = []
    for item in users:
        data.append(
            {
                "user_id": item.id,
                "telegram_id": item.telegram_id,
                "username": item.username,
            }
        )
    return data


@main_user_api.post("/set-user-online-status")
async def set_user_online_status(request: Request, data: UserListStatusDto):
    for item in data.data:
        user = await UserOrm.get(telegram_id=item.telegram_id)
        entity = await UserActivityStatusOrm.create(
            status="last",
            timestamp=datetime(
                year=item.date.year,
                month=item.date.month,
                day=item.date.day,
                hour=item.date.hour,
                minute=item.date.minute,
                second=item.date.second,
            ),
            user=user,
        )


@main_user_api.get("/link-stat-active")
async def get_active_link_stat(link_id: int):
    link = await InviteLinksOrm.get(id=link_id)
    channel = await link.channel.get()
    filtered_users = await get_users_with_link_and_enter_action(link_id)
    metrics = await get_user_metrics(filtered_users)
    metrics["channel"] = {
        "id": channel.id,
        "title": channel.title,
        "link": link.link,
    }
    return metrics
