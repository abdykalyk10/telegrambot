from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

# Создаем объект Router для обработки маршрутов
review_router = Router()


# Класс для описания состояний в процессе оставления отзыва
class RestourantReview(StatesGroup):
    name = State()
    age = State()
    phone_number = State()
    rate = State()
    extra_comments = State()


# Обработчик команды для начала отзыва
@review_router.message(Command("review"))
async def start_feedback(message: types.Message):
    await message.answer("Нажмите кнопку ниже, чтобы оставить отзыв:")


# Обработчик для начала сбора отзыва при нажатии кнопки
@review_router.callback_query(lambda c: c.data == 'review')
async def start_review(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("Как Вас зовут?")
    await state.set_state(RestourantReview.name)


# Обработчик для получения имени пользователя
@review_router.message(RestourantReview.name)
async def age(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Сколько вам лет?")
    await state.set_state(RestourantReview.age)


# Обработчик для получения возраста пользователя
@review_router.message(RestourantReview.age)
async def phone_number(message: types.Message, state: FSMContext):
    await state.update_data(age=message.text)
    await message.answer("Какой у вас номер телефона?")
    await state.set_state(RestourantReview.phone_number)


# Обработчик для получения номера телефона пользователя
@review_router.message(RestourantReview.phone_number)
async def rate(message: types.Message, state: FSMContext):
    await state.update_data(phone_number=message.text)
    await message.answer("Оцените наш ресторан от 1 до 5")
    await state.set_state(RestourantReview.rate)


# Обработчик для получения оценки от пользователя
@review_router.message(RestourantReview.rate)
async def comments(message: types.Message, state: FSMContext):
    await state.update_data(rate=message.text)
    await message.answer("Ваши дополнительные комментарии?")
    await state.set_state(RestourantReview.extra_comments)
