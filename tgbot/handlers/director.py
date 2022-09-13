from aiogram import types
from aiogram.dispatcher.filters.state import StatesGroup, State


class AdminStates(StatesGroup):
    get_worker_id = State()





async def dismiss_worker(message: types.Message):
    pass