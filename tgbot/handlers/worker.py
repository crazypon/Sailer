from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State


class SellItems(StatesGroup):
    get_item_id = State()
    get_item_quantity = State()


async def get_items(message: types.Message, repo):
    items = await repo.get_all_items()
    base_message = "<strong>Выберите товар, который хотите продать</strong>\n"
    for item in items:
        base_message += f"<code>{item[0]}. {item[1]}</code> - <strong>{item[2]}$</strong>\n"
    await message.answer(base_message, parse_mode="HTML")
    await SellItems.get_item_id.set()


async def select_item_id(message: types.Message, state: FSMContext, repo):
    item_id = message.text
    if item_id.isdigit():
        await message.answer("Введите количество товара")
        await state.update_data(item_id=int(item_id))
        await SellItems.next()
    else:
        await message.answer(f"Пожалуйста, отправьте количество в виде цифры")
        return


async def select_item_quantity(message: types.Message, state: FSMContext, repo):
    item_quantity = message.text
    if item_quantity.isdigit():
        purchase_data = await state.get_data()
        # TODO rid of commits in the next line
        seller_login = await repo.get_seller_login_with_user_id(int(message.from_user.id))
        await repo.save_purchase(purchase_data["item_id"], int(item_quantity), seller_login)
        await state.finish()
        await message.answer("Товар успешно продан")
    else:
        await message.answer(f"Пожалуйста, отправьте количество в виде цифры")
        return


def register_seller_handlers(dp: Dispatcher):
    dp.register_message_handler(get_items, is_worker=True, commands=["sell"])
    dp.register_message_handler(select_item_id, state=SellItems.get_item_id)
    dp.register_message_handler(select_item_quantity, state=SellItems.get_item_quantity)
