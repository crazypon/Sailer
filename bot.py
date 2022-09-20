import asyncio
import configparser
import logging
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from tgbot.teamstate_db.sql import create_pool
from tgbot.middlewares.getputcon import DBMiddleware
from tgbot.handlers.role_giver import register_role_giver_handlers
from tgbot.handlers.hr import register_hr_message_handlers
from tgbot.handlers.director import register_director_handlers
from tgbot.handlers.manager import register_manager_handlers
from tgbot.handlers.worker import register_seller_handlers
from tgbot.filters.filters import IsHRFilter, IsManagerFilter, IsDirectorFilter, IsWorkerFilter


logger = logging.getLogger(__name__)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    )
    logger.error("Starting bot")
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
    # registering role filters
    dp.bind_filter(IsDirectorFilter)
    dp.bind_filter(IsHRFilter)
    dp.bind_filter(IsManagerFilter)
    dp.bind_filter(IsWorkerFilter)

    # registering our handlers
    register_role_giver_handlers(dp)
    register_hr_message_handlers(dp)
    register_director_handlers(dp)
    register_manager_handlers(dp)
    register_seller_handlers(dp)

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
        logger.info('Bot stopped!')

