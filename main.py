from aiogram import Bot, Dispatcher
import asyncio

from baza.homiy import create_homiy_table
from baza.users import create_users_table
from baza.chanel import create_chanels_table
from middlewares import MultiCheckSubMiddleware
from config import TOKEN
import handlers
import logging

dp = Dispatcher()
dp.message.middleware.register(MultiCheckSubMiddleware())
dp.include_router(handlers.router)


async def startup_answer(bot: Bot):
    await create_chanels_table()
    await create_users_table()
    await create_homiy_table()
    await bot.send_message(652840346,"Bot ishga tushdi✅")

async def shutdown_answer(bot: Bot):
    await bot.send_message(652840346,"Bot to'xtadi❌")

async def start():

    dp.startup.register(startup_answer)
    dp.shutdown.register(shutdown_answer)


    bot = Bot(TOKEN)
    await dp.start_polling(bot)

asyncio.run(start())