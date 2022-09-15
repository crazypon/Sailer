from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State


class ManagerStates(StatesGroup):
    get_item_name = State()
    get_item_price = State()


async def