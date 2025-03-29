from dotenv import load_dotenv

load_dotenv()

import asyncio

from src.telegram_add_tool.bot.bot import dp, bot

async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
