import os
import hashlib
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram import types, Dispatcher
from aiogram.utils.callback_data import CallbackData


class AddNewWorker(StatesGroup):
    get_login = State()
    get_password = State()
    confirm_password = State()
    get_name = State()
    get_surname = State()
    get_post = State()


async def start_adding_worker(message: types.Message, state: FSMContext):
    await message.answer("Введите логин сотрудника")
    await AddNewWorker.get_login.set()


async def get_worker_login(message: types.Message, repo, state: FSMContext):
    login = message.text
    is_unique_login = await repo.check_worker_login(login)
    if is_unique_login:
        await state.update_data(worker_login=login)
        await message.answer("Введите пароль рабочего")
        await AddNewWorker.next()
    else:
        await message.answer("Это логин уже занят введите новый")
        return


async def get_worker_password(message: types.Message, state: FSMContext):
    await state.update_data(worker_password=message.text)
    await message.answer('Введите пароль второй раз')
    await AddNewWorker.next()


async def confirm_worker_password(message: types.Message, repo, state: FSMContext):
    raw_password = message.text
    worker_data = await state.get_data()
    worker_password = worker_data['worker_password']
    if worker_password == raw_password:
        salt = os.urandom(32)
        key = hashlib.pbkdf2_hmac("sha-256", raw_password.encode("utf-8"), salt, 10000)
        digest = (salt + key).hex()
        await state.update_data(worker_hash_password=digest)
        await message.answer("Введите имя рабочего")
        await AddNewWorker.next()
    else:
        await message.answer('Ваши пароли не совпадаю попробуйте заново при помощи /add_worker')
        return


async def get_worker_name(message: types.Message, state: FSMContext):
    worker_name = message.text
    await state.update_data(worker_name=worker_name)
    await message.answer("Введите фамилию рабочего")
    await AddNewWorker.next()


worker_post = CallbackData('worker', 'post')


async def get_worker_surname(message: types.Message, state: FSMContext):
    worker_surname = message.text
    await state.update_data(worker_surname=worker_surname)
    workers_post_markup = types.InlineKeyboardMarkup(row_width=2)
    worker_post_buttons = [
        types.InlineKeyboardButton(text="мэнэджер", callback_data=worker_post.new(post="manager")),
        types.InlineKeyboardButton(text="директор", callback_data=worker_post.new(post="director")),
        types.InlineKeyboardButton(text="продавец", callback_data=worker_post.new(post="seller")),
        types.InlineKeyboardButton(text="hr-щик", callback_data=worker_post.new(post="hr"))
    ]
    workers_post_markup.add(*worker_post_buttons)
    await message.answer("Введите должность сотрудника", reply_markup=workers_post_markup)
    await AddNewWorker.next()


async def get_worker_post(call: types.CallbackQuery, callback_data: dict, repo, state: FSMContext):
    await call.answer()
    worker_post_name = callback_data['post']
    worker_data = await state.get_data()
    await call.message.answer("рабочий успешно зарегестрирован!")
    worker_params = (
        worker_data["worker_login"], worker_data["worker_hash_password"],
        worker_data["worker_name"], worker_data["worker_surname"],
        worker_post_name
                     )
    await repo.add_worker(*worker_params)
    await state.finish()


def register_hr_message_handlers(dp: Dispatcher):
    dp.register_message_handler(start_adding_worker, state='*', is_hr=True, commands=['add_worker'])
    dp.register_message_handler(get_worker_login, state=AddNewWorker.get_login)
    dp.register_message_handler(get_worker_password, state=AddNewWorker.get_password)
    dp.register_message_handler(confirm_worker_password, state=AddNewWorker.confirm_password)
    dp.register_message_handler(get_worker_name, state=AddNewWorker.get_name)
    dp.register_message_handler(get_worker_surname, state=AddNewWorker.get_surname)
    dp.register_callback_query_handler(get_worker_post, worker_post.filter(), state=AddNewWorker.get_post)

