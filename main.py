import asyncio
import logging
from handlers.start import start_router
from bot_config import bot, dp
from handlers.my_info import myinfo_router
from handlers.random_name import random_name_router
from handlers.review_dialog import review_router


async def main():
    dp.include_router(start_router)
    dp.include_router(myinfo_router)
    dp.include_router(random_name_router)
    dp.include_router(review_router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
