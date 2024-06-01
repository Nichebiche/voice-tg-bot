import logging
import sys
import asyncio
from aiogram import Bot, Dispatcher
from config import settings
from handlers import router


async def main() -> None:
    bot = Bot(token=settings.telegram_token)
    dp = Dispatcher()
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())