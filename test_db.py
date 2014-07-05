import os
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from werkzeug.security import generate_password_hash, check_password_hash
from settings import DATABASE_URL



Base = declarative_base()
engine = create_engine(DATABASE_URL)
session = sessionmaker(engine)
session = session()


books_authors = Table('books_authors', Base.metadata,
    Column('author_id', Integer, ForeignKey('author.id'), primary_key=True),
    Column('book_id', Integer, ForeignKey('book.id'), primary_key=True)
)


class Book(Base):
    __tablename__ = 'book'
    id = Column(Integer, primary_key=True)
    title = Column(String(128), unique=True)
    authors = relationship('Author', secondary=books_authors, backref='book')

    def __init__(self, title):
        self.title = title

    def __repr__(self):
        return('Book {0}').format(self.title)



class Author(Base):
    __tablename__ = 'author'
    id = Column(Integer, primary_key=True)
    name = Column(String(64))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return('Author {0}').format(self.name)



class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    nickname = Column(String(32), unique=True)
    password = Column(String(128))

    def __init__(self, nickname, password):
        self.nickname = nickname
        self.password = self.hash_password(password)

    def hash_password(self, password):
        return generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


# u = User('freeman1', '111111')
# print u.password
# session.add(u)
# session.commit()
# u = session.query(User).filter_by(nickname='freeman1', password='111111')
u = session.query(User).filter_by(nickname='freeman1').first()
print u
print u.nickname
print u.password

print u.check_password('111111')