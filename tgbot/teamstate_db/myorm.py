import hashlib
from sqlalchemy import Column, String, BigInteger, SmallInteger, Integer, ForeignKey, Sequence, delete, insert
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import update
from sqlalchemy.future import select


Base = declarative_base()


class Worker(Base):
    __tablename__ = "workers"
    id = Column(Integer(), primary_key=True)
    # TODO make user_id column unique=True
    user_id = Column(Integer())
    login = Column(String(), unique=True)
    password_hash = Column(String(128))
    name = Column(String(128))
    surname = Column(String(128))
    post = Column(String(36))


class Item(Base):
    __tablename__ = "items"
    id = Column(Integer(), primary_key=True)
    item_name = Column(String(), unique=True)
    price = Column(BigInteger())


class Purchase(Base):
    __tablename__ = "purchases"
    id = Column(BigInteger(), primary_key=True)
    login = Column(String(), ForeignKey("workers.login"))
    sold_item_id = Column(Integer(), ForeignKey("items.id"))
    item_quantity = Column(Integer())
    # creating relationship
    relationship_for_worker = relationship('Worker')
    relationship_for_item = relationship('Item')


class DBCommands:
    def __init__(self, session):
        self.session = session

    async def get_users_password(self, login):
        stmt = select(Worker.password_hash).where(Worker.login == login)
        val = await self.session.execute(stmt)
        password_hash = val.scalar()
        return password_hash

    async def put_user_id(self, user_id, login):
        stmt = update(Worker).where(Worker.login == login).values(user_id=user_id)
        await self.session.execute(stmt)
        await self.session.commit()

    async def get_post_ids(self, post):
        # returns list of post ids
        stmt = select(Worker.user_id).where(Worker.post == post)
        val = await self.session.execute(stmt)
        user_vals = val.all()
        user_ids = []
        for item in user_vals:
            user_ids.append(item[0])
        return user_ids

    async def check_worker_login(self, login):
        stmt = select(Worker.login).where(Worker.login == login)
        val = await self.session.execute(stmt)
        login_db = val.scalar()
        if login_db:
            return False
        else:
            return True

    async def add_worker(self, login, password_hash, name, surname, post):
        self.session.add(Worker(
            login=login,
            password_hash=password_hash,
            name=name,
            surname=surname,
            post=post
        ))
        await self.session.commit()

    async def show_worker_list(self, only_seller=None):
        if only_seller:
            stmt = select(Worker.id, Worker.name, Worker.surname, Worker.post, Worker.login)
            stmt = stmt.where(Worker.post != "hr").where(Worker != "manager").where(Worker.post != "director")
            val = await self.session.execute(stmt)
            result = val.all()
            return result
        else:
            stmt = select(Worker.id, Worker.name, Worker.surname, Worker.post).where(Worker.post != "director")
            stmt = stmt.where(Worker.post != "hr")
            val = await self.session.execute(stmt)
            result = val.all()
            return result

    async def dismiss_worker(self, id):
        # deleting worker from worker list
        stmt = delete(Worker).where(Worker.id == id)
        await self.session.execute(stmt)
        await self.session.commit()

    async def put_item(self, name, price):
        stmt = self.session.add(Item(item_name=name, price=int(price)))
        await self.session.commit()

    async def get_sold_items(self, seller_login):
        stmt = select(Item.item_name, Item.price, Purchase.item_quantity).join(Purchase, Purchase.sold_item_id == Item.id)
        stmt = stmt.where(Purchase.login == seller_login)
        val = await self.session.execute(stmt)
        val = val.all()
        return val

    async def get_all_items(self):
        stmt = select(Item.id, Item.item_name, Item.price)
        val = await self.session.execute(stmt)
        res = val.all()
        return res

    async def get_employee_name(self, login):
        stmt = select(Worker.name, Worker.surname).where(Worker.login == login)
        val = await self.session.execute(stmt)
        res = val.all()
        return res

    async def get_seller_login(self, seller_id):
        stmt = select(Worker.login).where(Worker.id == seller_id)
        stmt = await self.session.execute(stmt)
        val = stmt.scalar()
        return val

    async def get_seller_login_with_user_id(self, seller_user_id):
        stmt = select(Worker.login).where(Worker.user_id == seller_user_id)
        stmt = await self.session.execute(stmt)
        val = stmt.scalar()
        return val

    async def save_purchase(self, item_id, item_quantity, login):
        stmt = insert(Purchase).values({"sold_item_id": item_id, "item_quantity": item_quantity, "login": login})
        await self.session.execute(stmt)
        await self.session.commit()
