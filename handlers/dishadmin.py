from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from bot_config import database
from datetime import datetime, timedelta

dishadmin_router = Router()

dishadmin_router.message.filter(F.from_user.id == 7886309988)


class Menu(StatesGroup):
    name_dish = State()
    price = State()
    description = State()
    category = State()


rating_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='первое', callback_data='rating:первое')],
        [InlineKeyboardButton(text='второе', callback_data='rating:второе')],
        [InlineKeyboardButton(text='пицца', callback_data='rating:пицца')],
        [InlineKeyboardButton(text='горячие напитки', callback_data='rating:горячие напитки')],
        [InlineKeyboardButton(text='холодные напитки', callback_data='rating:холодные напитки')],
        [InlineKeyboardButton(text='салаты', callback_data='rating:салаты')],
    ]
)


@dishadmin_router.message(Command('new_dish'))
async def name_dish(message: types.Message, state: FSMContext):
    await message.answer('Введите название блюды ')
    await state.set_state(Menu.name_dish)


@dishadmin_router.message(Menu.name_dish)
async def enter_price(message: types.Message, state: FSMContext):
    await state.update_data(name_dish=message.text)
    await message.answer('Введите цену блюда')
    await state.set_state(Menu.price)


@dishadmin_router.message(Menu.price)
async def description_dish(message: types.Message, state: FSMContext):
    price = message.text
    if not price.isdigit():
        await message.answer('Введите только число')
        return
    price = int(price)
    if price <= 0:
        await message.answer('Вводите цену больше "0"')
        return
    await state.update_data(price=price)
    await message.answer('Введите описание блюда')
    await state.set_state(Menu.description)


@dishadmin_router.message(Menu.description)
async def enter_category(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer('Введите категорию блюда', reply_markup=rating_kb)
    await state.set_state(Menu.category)


@dishadmin_router.callback_query(Menu.category)
async def finish(callback_query: types.CallbackQuery, state: FSMContext):
    category = callback_query.data.split(':')[1]
    await state.update_data(category=category)

    dish_data = await state.get_data()
    database.save_dish(dish_data)

    await callback_query.message.answer(
        f"Блюдо добавлено:\n"
        f"Название: {dish_data['name_dish']}\n"
        f"Цена: {dish_data['price']} сом\n"
        f"Описание: {dish_data['description']}\n"
        f"Категория: {dish_data['category']}"
    )
    await state.clear()

@dishadmin_router.message(Command('reviews'))
async def reviews_command(message: types.Message):
    reviews = database.get_reviews()
    reviews_text = "\n\n".join([f"Имя: {review['name']}\n"
                                f"Возраст: {review['age']}\n"
                                f"Телефон: {review['phone_number']}\n"
                                f"Оценка: {review['rate']}\n"
                                f"Комментарии: {review['extra_comments']}\n"
                                f"Дата: {review['date']}" for review in reviews])

    await message.answer(reviews_text)

