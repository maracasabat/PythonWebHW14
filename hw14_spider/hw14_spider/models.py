from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.schema import ForeignKey, Table
from sqlalchemy.orm import relationship

Base = declarative_base()

many_to_many = Table(
    'many_to_many',
    Base.metadata,
    Column('keywords_id', Integer, ForeignKey('keywords.id')),
    Column('quotes_id', Integer, ForeignKey('quotes.id'))
)


class Person(Base):
    __tablename__ = 'persons'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    author_name = Column(String(50), nullable=True)
    born_date = Column(String(50), nullable=True)
    born_location = Column(String(50), nullable=True)
    description = Column(String(50), nullable=True)


class Keywords(Base):
    __tablename__ = 'keywords'
    id = Column(Integer, primary_key=True)
    keyword = Column(String(50))


class Quotes(Base):
    __tablename__ = 'quotes'
    id = Column(Integer, primary_key=True)
    quote = Column(String(50))
    author = Column(String(50))
    keywords = relationship('Keywords', secondary=many_to_many, backref='keywords')


engine = create_engine('sqlite:///hw14.db', connect_args={'check_same_thread': False})
Base.metadata.create_all(engine)


