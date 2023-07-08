from sqlalchemy import ForeignKey, select, desc, Column, DateTime, Integer, ARRAY, String, create_engine, and_, func
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
import os
from dotenv import load_dotenv

load_dotenv()

engine = create_engine(os.environ.get('POSTGRES_STR'))

Base = declarative_base()


class CashBox(Base):
    __tablename__ = 'cash_box'

    id = Column(Integer, primary_key=True)
    date_work = Column(DateTime, nullable=False, unique=True)
    cash_in = Column(Integer, nullable=True)
    cash_out = Column(Integer, nullable=True)
    in_cash_box_sum = Column(Integer, nullable=True)
    employees = relationship('spendingsCashbox')


class spendingsCashbox(Base):
    __tablename__ = 'spendings_cash_box'

    id = Column(Integer, primary_key=True)
    date_work_id = Column(Integer, ForeignKey('cash_box.id'))
    date_work = relationship('CashBox')


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, nullable=False, unique=True)
    status = Column(String, nullable=False)
    phone_number = Column(String, nullable=True)
    feedback = Column(ARRAY(String))


Session = sessionmaker(bind=engine)

Base.metadata.create_all(engine)
