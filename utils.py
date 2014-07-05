import re
from flask import abort, flash, redirect, url_for, request
from flask import session as f_session
from functools import wraps
from models import User, session



def str_separator(string):
    return re.findall('\w+ *\w+', string)


def get_or_create(model, **params):
    instance = session.query(model).filter_by(**params).first()
    if instance:
        return instance
    else:
        instance = model(**params)
        session.add(instance)
        return instance

def get_or_404(model, **params):
    instance = session.query(model).filter_by(**params).first()
    if instance:
        return instance
    else:
        return abort(404)

def get_authors(book, format):
    authors = []
    for author in book.authors:
        authors.append(author.name)        
    if format == 'str':
        authors = ', '.join(authors)
    return authors

def get_books(author, format):
    books = []
    for book in author.books:
        books.append(book.title)
    if format == 'str':
        books = ', '.join(books)
    return books

def diff_list(l1, l2):
    '''
    l1 is original list, l2 is modified list.
    Return rm_lst and append_lst to remove and append data for resultant list. 
    '''
    # diff befor, after
    diff = list(set(l1) & set(l2))

    # rm_lst is what remove in original list l1
    if not diff:
        rm_lst = l1
    else:
        rm_lst = list(set(l1) - set(diff))

    # append_lst is what append to original list 1
    append_lst = list(set(l2) - set(l1))

    return(rm_lst, append_lst)

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'nickname' in f_session.keys():
            return f(*args, **kwargs)
        else:
            flash('Login required')
            return redirect(url_for('login'))
    return wrapper

def is_auth(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'nickname' in f_session.keys():
            msg = 'Logged in as <strong class=badge>{0}</strong>'.format(f_session['nickname'])
            flash(msg)
            return redirect(url_for('index'))
        else:
            return f(*args, **kwargs)
    return wrapper