from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext


class AdminStates(StatesGroup):
    get_worker_id = State()
    get_seller_id = State()


async def get_worker_list(message: types.Message, repo):
    res = await repo.show_worker_list()
    base_message = "<strong>Список сотрудников</strong>: \n\n"
    for worker in res:
        worker_info = f"<code>{worker[0]}. {worker[1]} {worker[2]}</code> - <strong>{worker[3]}</strong> \n"
        base_message += worker_info
    await message.answer(base_message, parse_mode="HTML")


async def dismiss_worker(message: types.Message, repo):
    res = await repo.show_worker_list()
    base_message = "<strong>Список сотрудников</strong>: \n\n"
    for worker in res:
        worker_info = f"<code>{worker[0]}. {worker[1]} {worker[2]}</code> - <strong>{worker[3]}</strong> \n"
        base_message += worker_info
    base_message += "\n"
    base_message += "Отправьте id сотрудника которого хотите уволить."
    await message.answer(base_message, parse_mode="HTML")
    await AdminStates.get_worker_id.set()


async def list_all_sellers(message: types.Message, repo):
    res = await repo.show_worker_list(only_seller=True)
    base_message = "<strong>Список продавцов</strong>: \n\n"
    for worker in res:
        worker_info = f"<code>{worker[0]}. {worker[1]} {worker[2]}</code>\n"
        base_message += worker_info
    base_message += "\n"
    base_message += "Отправьте id сотрудника, чтобы посмотреть отчёт о продажах."
    await message.answer(base_message, parse_mode="HTML")
    await AdminStates.get_seller_id.set()


async def see_financial_report(message: types.Message, state: FSMContext, repo):
    seller_id = int(message.text)
    seller_login = await repo.get_seller_login(seller_id)
    employee_name = await repo.get_employee_name(seller_login)
    sold_items = await repo.get_sold_items(seller_login)
    base_message = f"Финансовый отчёт {employee_name[0]} {employee_name[1]}\n"
    final_price = 0
    for item in sold_items:
        item_row = f"<code>{item[0]}</code> - <strong>{item[1]}</strong>\n"
        base_message += item_row
        final_price += item[1]
    base_message += f"<strong>Итого: <code>{final_price} uzs</code></strong>\n"
    await message.answer(base_message, parse_mode="HTML")
    await state.finish()


async def dismiss_worker_id(message: types.Message, state: FSMContext, repo):
    worker_id = message.text
    await repo.dismiss_worker(int(worker_id))
    await message.answer('Сотрудник успешно удалён!')
    await state.finish()


def register_director_handlers(dp: Dispatcher):
    dp.register_message_handler(get_worker_list, is_director=True, commands=["list"], state="*")
    dp.register_message_handler(dismiss_worker, is_director=True, commands=["dismiss"], state="*")
    dp.register_message_handler(dismiss_worker_id, state=AdminStates.get_worker_id)
