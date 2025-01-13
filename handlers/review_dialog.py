from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

review_router = Router()

class RestourantReview(StatesGroup):
    name = State()
    age = State()
    phone_number = State()
    rate = State()
    extra_comments = State()

user_id = []

@review_router.callback_query(F.data == "review")
async def check_id(call: types.CallbackQuery, state: FSMContext):
    if call.message.from_user.id in user_id:
        await call.message.answer("Нельзя оставлять отзыв более одного раза.")
        await state.clear()
    else:
        user_id.append(call.message.from_user.id)
        await call.message.answer("Как Вас зовут?")
        await state.set_state(RestourantReview.name)

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
    await message.answer("Оцените наш ресторан от 1 до 5")
    await state.set_state(RestourantReview.rate)

@review_router.message(RestourantReview.rate)
async def comments(message: types.Message, state: FSMContext):
    await state.update_data(rate=message.text)
    await message.answer("Ваши дополнительные комментарии?")
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
    await state.clear()
