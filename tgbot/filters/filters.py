from aiogram.dispatcher.filters import BoundFilter
from aiogram.dispatcher.handler import ctx_data
from aiogram import types


class IsDirectorFilter(BoundFilter):
    '''
    custom is director filter
    '''
    key = 'is_director'

    def __init__(self, is_director):
        self.is_director = is_director

    async def check(self, message: types.Message):
        # getting repo
        data = ctx_data.get()
        repo = data.get("repo")
        director_ids = await repo.get_post_ids("director")
        return message.from_user.id in director_ids


class IsManagerFilter(BoundFilter):
    '''
    custom is manager filter
    '''
    key = 'is_manager'

    def __init__(self, is_manager):
        self.is_manager = is_manager

    async def check(self, message: types.Message):
        # getting repo
        data = ctx_data.get()
        repo = data.get("repo")
        is_manager = await repo.get_post_ids("manager")
        return message.from_user.id in is_manager


class IsWorkerFilter(BoundFilter):
    '''
    custom is worker filter
    '''
    key = 'is_worker'

    def __init__(self, is_worker):
        self.is_worker = is_worker

    async def check(self, message: types.Message):
        # getting repo
        data = ctx_data.get()
        repo = data.get("repo")
        worker_ids = await repo.get_post_ids("worker")
        return message.from_user.id in worker_ids


class IsHRFilter(BoundFilter):
    '''
    custom is hr filter
    '''
    key = 'is_hr'

    def __init__(self, is_hr):
        self.is_hr = is_hr

    async def check(self, message: types.Message):
        # getting repo
        data = ctx_data.get()
        repo = data.get("repo")
        hr_ids = await repo.get_post_ids("hr")
        return message.from_user.id in hr_ids
