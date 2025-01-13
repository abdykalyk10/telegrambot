from aiogram import Router, types
from aiogram.filters import Command

start_router = Router()


@start_router.message(Command("start"))
async def start_command(message: types.Message):
    greeting = (
        f"Привет, {message.from_user.first_name}!\n"
        f"Мои команды:\n"
        f"/start - начать работу с ботом\n"
        f"/random - случайное имя\n"
        f"/myinfo - информация о пользователе"
    )
    kb = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [types.InlineKeyboardButton(text='Оставить отзыв', callback_data='review'), ]
        ]
    )
    await message.reply(greeting, reply_markup=kb)
