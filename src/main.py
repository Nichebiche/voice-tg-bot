import logging
import asyncio
from aiogram import Bot, Dispatcher
from config import config
from handlers import router
from openai_client import init_client

async def main() -> None:
    bot = Bot(token=config.telegram_token.get_secret_value())
    dp = Dispatcher()
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        handlers=[
                            logging.FileHandler("log.log", mode="w"),
                            logging.StreamHandler()
                        ]
    )
    logger = logging.getLogger('__name__')
    
    asyncio.run(main())