import hashlib
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State


class RoleAssigner(StatesGroup):
    get_login = State()
    get_password = State()


async def start_checking_user(message: types.Message):
    await message.answer('Здравствуйте, введите логин')
    await RoleAssigner.get_login.set()


async def check_login(message: types.Message, state: FSMContext, repo):
    login = message.text
    user = await repo.check_worker_login(login)
    if not user:
        await message.answer("Введите пароль")
        await state.update_data(login=login)
        await RoleAssigner.get_password.set()
    else:
        await message.answer("Вы ввели не правильный логин")
        return


async def check_password(message: types.Message, state: FSMContext, repo):
    raw_password = message.text
    data = await state.get_data()
    login = data['login']
    # rehashing password
    worker_password_hash = await repo.get_users_password(login)
    salt = bytes.fromhex(worker_password_hash)[:32]
    key = hashlib.pbkdf2_hmac("sha-256", raw_password.encode('utf-8'), salt, 10000)
    entered_password_hash = (salt + key).hex()
    if worker_password_hash == entered_password_hash:
        await message.answer("Вы успешно вошли в вашу учетную запись!")
        await repo.put_user_id(message.from_user.id, login)
        await message.delete()
        await state.finish()
    else:
        await message.answer("Неправильный пароль! Ввведите заново")
        return


def register_role_giver_handlers(dp: Dispatcher):
    dp.register_message_handler(start_checking_user, commands=["start"])
    dp.register_message_handler(check_login, state=RoleAssigner.get_login)
    dp.register_message_handler(check_password, state=RoleAssigner.get_password)
