import logging
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker


logging.basicConfig(
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
)


async def create_pool(user, password, host, database):
    engine = create_async_engine(
        f"postgresql+asyncpg://{user}:{password}@{host}/{database}"
    )
    async_session_maker = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
    async_session = async_session_maker()
    return async_session
