from flask import views, request, render_template, url_for, flash, abort, redirect
from flask import session as f_session
from models import *
from forms import SignUpForm, LogInForm, AddAuthorForm, AddBookForm, EditBookForm, \
                  EditAuthorForm
from utils import str_separator, get_or_create, get_or_404, get_authors, diff_list, \
                  get_books, login_required, is_auth



# engine = create_engine(DATABASE_URL)
# session = sessionmaker(engine)
# session = session()



class Index(views.MethodView):
    def get(self):
        # sort books by author
        if request.args.get('author'):
            author = get_or_404(Author, name=request.args.get('author'))
            books = author.books
        
        # get all books
        else:
            books = session.query(Book).all()
        
        return render_template('index.haml', books=books)



class Search(views.MethodView):
    def post(self):
        query = '%{0}%'.format(request.form['query'])
        
        # get the books containing query argument in the title
        books = session.query(Book).filter(Book.title.like(query)).all()
        
        if books == []:
            # get the authors containing query argument in the title
            authors = session.query(Author).filter(Author.name.like(query)).all()
            books = list(set([x for a in authors for x in a.books]))
        return render_template('index.haml', books=books)



class SignUp(views.MethodView):
    @is_auth
    def get(self):
        form = SignUpForm()
        return render_template('signup.haml', form=form)

    def post(self):
        form = SignUpForm()
        if form.validate():
            if session.query(User).filter_by(nickname=form.nickname.data).count() == 0:
                session.add(User(nickname=form.nickname.data, password=form.password.data))
                session.commit()
                msg = 'Thanks for registering <strong class=badge>{0}</strong>.  \
                       Please sign in'.format(form.nickname.data)
                flash(msg)
                return redirect(url_for('login'))
            else:
                msg = 'User <strong class=badge>{0}</strong> already \
                       exists.'.format(form.nickname.data)
                flash(msg)
        return render_template('signup.haml', form=form)



class LogIn(views.MethodView):
    @is_auth
    def get(self):
        form = LogInForm()
        return render_template('login.haml', form=form)

    def post(self):
        if 'logout' in request.form:
            f_session.pop('nickname', None)
            flash('You have been logged out')
            return redirect(url_for('index'))
        form = LogInForm()
        if form.validate():
            u = session.query(User).filter_by(nickname=form.nickname.data).first()
            if u is not None and u.check_password(form.password.data):
                f_session['nickname'] = u.nickname
                msg = 'Wellcome <strong class=badge>{0}</strong>!'.format(u.nickname)
                flash(msg)
                return redirect(url_for('index'))
            else:
                flash('Wrong nickname or password')
                return redirect(url_for('index'))
        return render_template('login.haml', form=form)



class AddAuthor(views.MethodView):
    def get(self):
        form = AddAuthorForm()
        return render_template('add_author.haml', form=form)

    def post(self):
        form = AddAuthorForm()
        if form.validate():
            # if session.query(Author).filter_by(name=form.name.data).count() == 0:
            author = get_or_create(Author, name=form.name.data)
            for title in str_separator(form.title.data):
                author.books.append(get_or_create(Book, title=title))
            session.commit()
            return redirect(url_for('add_author'))
        else:
            msg = 'Author <strong class=badge>{0}</strong> already \
                   exists!'.format(form.name.data)
            flash(msg)
        return render_template('add_author.haml', form=form)


class AddBook(views.MethodView):
    def get(self):
        form = AddBookForm()
        return render_template('add_book.haml', form=form)

    def post(self):
        form = AddBookForm()
        if form.validate():
            if session.query(Book).filter_by(title=form.title.data).count() == 0:
                print form.title.data
                book = get_or_create(Book, title=form.title.data)
                for name in str_separator(form.name.data):
                    book.authors.append(get_or_create(Author, name=name))
                session.commit()
                msg = 'Book <strong class=badge>{0}</strong> added!'.format(form.title.data)
                flash(msg)
                return redirect(url_for('add_book'))
            else:
                msg = 'Book <strong class=badge>{0}</strong> already \
                       exists!'.format(form.title.data)
                flash(msg)
        return render_template('add_book.haml', form=form)




class EditBook(views.MethodView):
    @login_required
    def get(self, title):
        form = EditBookForm()
        book = get_or_404(Book, title=title)
        form.title.data = book.title
        form.name.data = get_authors(book, format='str')
        return render_template('edit_book.haml', form=form, title=title)

    @login_required
    def post(self, title):
        book = get_or_404(Book, title=title)
        form = EditBookForm()
        if form.validate():
            if book.title != form.title.data:
                book.title = form.title.data
                try:
                    session.commit()
                except:
                    session.rollback()
                    msg = 'Book <strong class=badge>{0}</strong> already \
                           exists!'.format(form.title.data)
                    flash(msg)
                    # return render_template('edit_book.haml', form=form, title=title)
                    return self.get(title)

            # Get current and changed list of authors.
            new_authors = str_separator(form.name.data)
            old_authors = get_authors(book, format='list')

            # We get authors' names which have to be deleted from an original list 
            # and also authors' names which have to be added.
            rm_lst, append_lst = diff_list(old_authors, new_authors)

            # remove not related authors
            for name in rm_lst:
                a = get_or_404(Author, name=name)
                book.authors.remove(a)
                if len(a.books) == 1:
                    session.delete(a)
            
            # relate new authors with exist book
            for name in append_lst:
                a = get_or_create(Author, name=name)
                book.authors.append(a)
            session.commit()

            return redirect(url_for('index'))
        return render_template('edit_book.haml', form=form, title=title)




class EditAuthor(views.MethodView):
    @login_required
    def get(self, name):
        form = EditAuthorForm()
        author = get_or_404(Author, name=name)
        form.name.data = author.name
        form.title.data = get_books(author, format ='str')
        return render_template('edit_author.haml', form = form, name=name)

    @login_required
    def post(self, name):
        print name
        form = EditAuthorForm()
        author = get_or_404(Author, name=name)
        if form.validate():
            if author.name != form.name.data:
                author.name = form.name.data
                try:
                    session.commit()
                except:
                    session.rollback()
                    msg = 'Author <strong class=badge>{0}</strong> already \
                           exists!'.format(form.name.data)
                    flash(msg)
                    # return render_template('edit_author.haml', form=form, name=name)
                    return self.get(name)
            
            new_books = str_separator(form.title.data)
            old_books = get_books(author, format='list')

            # get what to delete from exists books list and what to add, to bring
            # to edited field books
            rm_lst, append_lst = diff_list(old_books, new_books)
            print(rm_lst, append_lst)

            # remove not related books
            for title in rm_lst:
                b = get_or_404(Book, title=title)
                author.books.remove(b)
                if len(b.authors) == 1:
                    session.delete(b)
            
            # relate new books with exist author
            for title in append_lst:
                b = get_or_create(Book, title=title)
                author.books.append(b)
            session.commit()

            return redirect(url_for('index'))
        return render_template('edit_author.haml', form=form, name=name)



class RemoveAuthor(views.MethodView):
    @login_required
    def get(self, name):
        author = get_or_404(Author, name=name)
        session.delete(author)
        session.commit()
        return redirect(url_for('index'))



class RemoveBook(views.MethodView):
    @login_required
    def get(self, title):
        book = get_or_404(Book, title=title)
        session.delete(book)
        session.commit()
        return redirect(url_for('index'))
