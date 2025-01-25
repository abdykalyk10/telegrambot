from aiogram import Router, F, types
from bot_config import database

dishes_router = Router()


@dishes_router.callback_query(F.data == 'dishes')
async def all_dishes(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.answer('Меню:')
    dishes = database.get_dishes()
    sorted_dishes = sorted(dishes, key=lambda dish: dish.get('name_dish').lower())
    for dish in sorted_dishes:
        await callback.message.answer(
            f"Название: {dish.get('name_dish', 'Без названия')}\n"
            f"Цена: {dish.get('price', 'Цена не указана')} сом\n"
            f"Описание: {dish.get('description', 'Нет описания блюда')}\n"
            f"Категория: {dish.get('category', 'Нет категории')}"
        )
