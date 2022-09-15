from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State


class  SellItems(StatesGroup):
    get_item_id = State()
    get_item_quantity = State()


async def get_items(message: types.Message, repo):
