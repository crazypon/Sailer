from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State


class ManagerStates(StatesGroup):
    get_item_name = State()
    get_item_price = State()


async def get_item_name_start(message: types.Message):
    await message.answer('Введите название товара')
    await ManagerStates.get_item_name.set()


async def get_item_name(message: types.Message, state: FSMContext):
    item_name = message.text
    await state.update_data(item_name=item_name)
    await message.answer("Введите стоимость товара")
    await ManagerStates.next()


async def get_item_price(message: types.Message, state: FSMContext, repo):
    item_data = await state.get_data()
    item_price = message.text
    await repo.put_item(item_data["item_name"], item_price)
    await message.answer("Товар успешно добавлен в базу данных")
    await state.finish()


def register_manager_handlers(dp: Dispatcher):
    dp.register_message_handler(get_item_name_start, is_manager=True, commands=['add_item'], state="*")
    dp.register_message_handler(get_item_name, state=ManagerStates.get_item_name)
    dp.register_message_handler(get_item_price, state=ManagerStates.get_item_price)
