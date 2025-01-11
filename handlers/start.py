from aiogram import Router, types
from aiogram.filters import Command

start_router = Router()

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


@start_router.message(Command("start"))
async def start_command(message: types.Message):
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
