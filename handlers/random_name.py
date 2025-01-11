from aiogram import Router, types
from aiogram.filters import Command
import random

random_name_router = Router()


@random_name_router.message(Command("random"))
async def random_command(message: types.Message):
    names = ("Гути", "Игорь", "Гарри", "Кевин", "Александр")
    random_name = random.choice(names)
    await message.reply(f"Случайное имя: {random_name}")
