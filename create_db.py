import os, random
from models import *
from utils import get_or_create



Base.metadata.create_all(engine)


def build_db():
    '''
    Build a small db with some example entries.

    '''

    names = [
        'Oleg', 'Mark', 'William', 'James', 'Harry', 'Amelia', 'Oliver', 'Jack', 'John'
    ]

    books = [
        'MySQL for Python', 'MySQL Cookbook', 'Essential SQLAlchemy', 'Learning Python',
        'Python for Data Analysis', 'Core Python Applications Programming', 'Python Algorithms'
        'Think Python', 'Computer Games with Python', 'MongoDb in action'
    ]

    user = {'name': 'user', 'passwd': 'like-books'}

    counter = session.query(Author).count()

    if not counter:
        for i in range(len(names)):
            author = get_or_create(Author, name=names[i])
            author.books.append(get_or_create(Book, title=books[i]))
            author.books.append(get_or_create(Book, title=random.choice(books)))
            session.commit()

        session.add(User(nickname=user['name'], password=user['passwd']))
        session.commit()

build_db()
