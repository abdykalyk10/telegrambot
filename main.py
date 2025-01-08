import random
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
from dotenv import load_dotenv
import asyncio
import os

load_dotenv()
BOT_TOKEN = os.getenv("TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

USER_SET_FILE = "unique_users.txt"

def load_unique_users():
    try:
        with open(USER_SET_FILE, "r") as file:
            return set(map(int, file.read().splitlines()))
    except FileNotFoundError:
        return set()

def save_unique_users(users):
    with open(USER_SET_FILE, "w") as file:
        file.write("\n".join(map(str, users)))

unique_users = load_unique_users()

@dp.message(Command("start"))
async def start_command(message: Message):
    user_id = message.from_user.id

    is_new_user = user_id not in unique_users
    if is_new_user:
        unique_users.add(user_id)
        save_unique_users(unique_users)

    total_users = len(unique_users)

    greeting = (
        f"Привет, {message.from_user.first_name}!\n"
        f"Наш бот обслуживает уже {total_users} пользователей.\n\n"
        f"Мои команды:\n"
        f"/start - начать работу с ботом\n"
        f"/random - случайное имя\n"
        f"/myinfo - информация о пользователе"
    )
    await message.reply(greeting)

@dp.message(Command("myinfo"))
async def myinfo_command(message: Message):
    user_info = (
        f"Ваш id: {message.from_user.id}\n"
        f"Ваше имя: {message.from_user.first_name}\n"
        f"Ваш ник: @{message.from_user.username if message.from_user.username else 'не указан'}"
    )
    await message.reply(user_info)

@dp.message(Command("random"))
async def random_command(message: Message):
    names = ("Гути", "Игорь", "Гарри", "Кевин", "Александр")
    random_name = random.choice(names)
    await message.reply(f"Случайное имя: {random_name}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
