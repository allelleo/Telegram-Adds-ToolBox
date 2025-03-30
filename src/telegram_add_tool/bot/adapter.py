import httpx

from src.telegram_add_tool.bot.config import BACKEND_URL


async def check_user_access(user_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BACKEND_URL}/api/v1/user/check-user-access?telegram_id={user_id}"
        )
    if response.status_code == 200:
        user_name = response.json()["name"]
        return user_name
    else:
        if response.status_code == 404:
            return False
        else:
            return response.status_code, response.text


async def get_channels_adapter():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BACKEND_URL}/api/v1/user/channels")
    if response.status_code == 200:
        channels = response.json()
        return channels
    else:
        return response.status_code, response.text

async def get_channel_info(channel_id):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BACKEND_URL}/api/v1/user/get-chanel-info?channel_id={channel_id}")
    if response.status_code == 200:
        channel = response.json()
        return channel
    else:
        return response.status_code, response.text