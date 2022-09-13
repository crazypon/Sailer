from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware
from tgbot.teamstate_db.myorm import DBCommands


class DBMiddleware(LifetimeControllerMiddleware):
    def __init__(self, session):
        super().__init__()
        self.session = session

    async def pre_process(self, obj, data, *args):
        data["repo"] = DBCommands(self.session)

    async def post_process(self, obj, data, *args):
        del data["repo"]