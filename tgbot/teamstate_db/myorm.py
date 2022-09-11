from sqlalchemy import Column, String, BigInteger, Integer,ForeignKey, Sequence, delete
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import update


Base = declarative_base()


class Worker(Base):
    __tablename__ = "workers"
    id = Column(Integer(), Sequence("worker_id_seq"), primary_key=True)
    login = Column(String(), unique=True)
    password_hash = Column(String(128))
    name = Column(String(128))
    surname = Column(String(128))


class Item(Base):
    __tablename__ = "items"
    id = Column(Integer(), Sequence("ite_id_seq"), primary_key=True)
    item_name = Column(String(), unique=True)
    price = Column(BigInteger())


class Purchase(Base):
    __tablename__ = "purchases"
    id = Column(BigInteger(), Sequence("sold_items_seq"), primary_key=True)
    login = Column(String(), ForeignKey("workers.login"), unique=True)
    sold_item_id = Column(Integer(), ForeignKey("items.id"))
    # creating relationship
    relationship_for_worker = relationship('Worker')
    relationship_for_item = relationship('Item')
