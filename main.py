import asyncio
import logging
from aiogram import Bot
from handlers.start import start_router
from bot_config import bot, dp, database
from handlers.my_info import myinfo_router
from handlers.random_name import random_name_router
from handlers.review_dialog import review_router
from handlers.dishadmin import dishadmin_router
from handlers.dishes import dishes_router, all_dishes
from handlers.bot_ban import ban_ruter

async def on_startup(bot: Bot):

     database.create_table()


async def main():
    dp.include_router(start_router)
    dp.include_router(myinfo_router)
    dp.include_router(random_name_router)
    dp.include_router(review_router)
    dp.startup.register(on_startup)
    dp.include_router(dishadmin_router)
    dp.include_router(dishes_router)
    dp.include_router(ban_ruter)
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
