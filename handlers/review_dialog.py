from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command

from bot_config import database

review_router = Router()


class RestourantReview(StatesGroup):
    name = State()
    age = State()
    phone_number = State()
    rate = State()
    extra_comments = State()


rating_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='1', callback_data='rating:1'),
            InlineKeyboardButton(text='2', callback_data='rating:2'),
            InlineKeyboardButton(text='3', callback_data='rating:3'),
            InlineKeyboardButton(text='4', callback_data='rating:4'),
            InlineKeyboardButton(text='5', callback_data='rating:5'),
        ]
    ]
)

user_id_set = set()


@review_router.callback_query(F.data == "review")
async def check_id(call: types.CallbackQuery, state: FSMContext):
    user_id_value = call.from_user.id
    if user_id_value in user_id_set:
        await call.message.answer("Нельзя оставлять отзыв более одного раза.")
        await state.clear()
    else:
        user_id_set.add(user_id_value)
        await state.update_data(user_id=user_id_value)
        await call.message.answer('Можете остановить диалог введя "/stop" или "стоп"')
        await call.message.answer("Как Вас зовут?")
        await state.set_state(RestourantReview.name)


@review_router.message(Command('stop'))
@review_router.message(F.text == 'стоп')
async def stop_dialog(message: types.Message, state: FSMContext):
    await message.answer('Диалог остановлен')
    await state.clear()


@review_router.message(RestourantReview.name)
async def age(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Сколько вам лет?")
    await state.set_state(RestourantReview.age)


@review_router.message(RestourantReview.age)
async def phone_number(message: types.Message, state: FSMContext):
    await state.update_data(age=message.text)
    await message.answer("Какой у вас номер телефона?")
    await state.set_state(RestourantReview.phone_number)


@review_router.message(RestourantReview.phone_number)
async def rate(message: types.Message, state: FSMContext):
    await state.update_data(phone_number=message.text)
    await message.answer("Оцените наш ресторан от 1 до 5", reply_markup=rating_kb)
    await state.set_state(RestourantReview.rate)


@review_router.callback_query(RestourantReview.rate)
async def handle_rating(call: types.CallbackQuery, state: FSMContext):
    rating = call.data.split(':')[1]
    await state.update_data(rate=rating)
    await call.message.answer("Ваши дополнительные комментарии?")
    await state.set_state(RestourantReview.extra_comments)


@review_router.message(RestourantReview.extra_comments)
async def end_review(message: types.Message, state: FSMContext):
    await state.update_data(extra_comments=message.text)
    review_data = await state.get_data()

    await message.answer(
        f"Спасибо за ваш отзыв!\n\n"
        f"Имя: {review_data['name']}\n"
        f"Возраст: {review_data['age']}\n"
        f"Телефон: {review_data['phone_number']}\n"
        f"Оценка: {review_data['rate']}\n"
        f"Комментарии: {review_data['extra_comments']}"
    )
    database.save_complaint(review_data)
    await state.clear()
