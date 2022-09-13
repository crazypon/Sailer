import asyncio
import configparser
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from tgbot.teamstate_db.sql import create_pool
from tgbot.middlewares.getputcon import DBMiddleware
from tgbot.teamstate_db.myorm import DBCommands
from tgbot.filters.filters import IsDirectorFilter
from tgbot.handlers.role_giver import register_role_giver_handlers


async def main():
    config = configparser.ConfigParser()
    config.read("bot.ini")
    redis_storage = RedisStorage2(port=6379, host='localhost')
    bot = Bot(token=config['tg_bot']['token'])
    dp = Dispatcher(bot=bot, storage=redis_storage)

    # registering our middlewares
    dp.middleware.setup(DBMiddleware(
        await create_pool(
                user=config['db']['user'],
                password=config['db']['password'],
                host=config['db']['host'],
                database=config['db']['database']
            )
    ))

    # rep = DBCommands(session_pool)
    # dp.bind_filter(IsDirectorFilter(rep))

    # registering our handlers
    register_role_giver_handlers(dp)

    try:
        await dp.start_polling()
    finally:
        await bot.get_session()


if __name__ == "__main__":
    try:
        loop = asyncio.get_event_loop()
        task = loop.create_task(main())
        loop.run_forever()
    except KeyboardInterrupt:
        print("stop")

