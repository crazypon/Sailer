from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State


class ManagerStates(StatesGroup):
    get_item_name = State()
    get_item_price = State()
    get_seller_id = State()


async def get_item_name_start(message: types.Message):
    await message.answer('Введите название товара')
    await ManagerStates.get_item_name.set()


async def get_item_name(message: types.Message, state: FSMContext):
    item_name = message.text
    if item_name.isdigi():
        await message.answer('Пожалуйста введите нормальное название товара')
        return
    else:
        await state.update_data(item_name=item_name)
        await message.answer("Введите стоимость товара")
        await ManagerStates.next()


async def get_item_price(message: types.Message, state: FSMContext, repo):
    item_data = await state.get_data()
    item_price = message.text
    if item_price.isdigit():
        await repo.put_item(item_data["item_name"], item_price)
        await message.answer("Товар успешно добавлен в базу данных")
        await state.finish()
    else:
        await message.answer("Пожалуйста введите цену товара в виде цифр")
        return


async def list_all_sellers(message: types.Message, repo):
    res = await repo.show_worker_list(only_seller=True)
    base_message = "<strong>Список продавцов</strong>: \n\n"
    for worker in res:
        worker_info = f"<code>{worker[0]}. {worker[1]} {worker[2]}</code>\n"
        base_message += worker_info
    base_message += "\n"
    base_message += "Отправьте id сотрудника, чтобы посмотреть отчёт о продажах."
    await message.answer(base_message, parse_mode="HTML")
    await ManagerStates.get_seller_id.set()


async def see_financial_report(message: types.Message, state: FSMContext, repo):
    seller_id = message.text
    if seller_id.isdigit():
        seller_login = await repo.get_seller_login(int(seller_id))
        if seller_login:
            employee_name = await repo.get_employee_name(seller_login)
            sold_items = await repo.get_sold_items(seller_login)
            base_message = f"Финансовый отчёт {employee_name[0][0]} {employee_name[0][1]}\n"
            final_price = 0
            for item in sold_items:
                item_row = f"<code>{item[0]}</code> - <strong>{item[1]}</strong>\n"
                base_message += item_row
                final_price += item[1] * item[2]
            base_message += f"<strong>Итого: <code>{final_price} uzs</code></strong>\n"
            await message.answer(base_message, parse_mode="HTML")
            await state.finish()
        else:
            await message.answer("Вы отправили несуществующий id")
    else:
        await message.answer("id должен быть в виде цифры")


def register_manager_handlers(dp: Dispatcher):
    dp.register_message_handler(get_item_name_start, is_manager=True, commands=['add_item'], state="*")
    dp.register_message_handler(get_item_name, state=ManagerStates.get_item_name)
    dp.register_message_handler(get_item_price, state=ManagerStates.get_item_price)
    dp.register_message_handler(list_all_sellers, is_manager=True, commands=["report"], state="*")
    dp.register_message_handler(see_financial_report, state=ManagerStates.get_seller_id)
