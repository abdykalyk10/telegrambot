from aiogram import Router, F, types
from bot_config import database
from aiogram_widgets.pagination import TextPaginator

dishes_router = Router()


@dishes_router.callback_query(F.data == 'dishes')
async def all_dishes(callback: types.CallbackQuery):
    await callback.answer()

    dishes = database.get_dishes()
    sorted_dishes = sorted(dishes, key=lambda dish: dish.get('name_dish').lower())

    text_data = [
        f"Название: {dish.get('name_dish', 'Без названия')}\n"
        f"Цена: {dish.get('price', 'Цена не указана')} сом\n"
        f"Описание: {dish.get('description', 'Нет описания блюда')}\n"
        f"Категория: {dish.get('category', 'Нет категории')}"
        for dish in sorted_dishes
    ]

    paginator = TextPaginator(data=text_data, router=dishes_router, per_page=1)

    current_text_chunk, reply_markup = paginator.current_message_data

    await callback.message.answer(
        text=current_text_chunk,
        reply_markup=reply_markup
    )
