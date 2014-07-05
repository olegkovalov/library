from flask import Flask
from werkzeug import ImmutableDict
from settings import secret_key, TEMPLATE_FOLDER
from create_db import build_db

# Views
from views import *

class FlaskWithHamlish(Flask):
    jinja_options = ImmutableDict(
        extensions=['jinja2.ext.autoescape', 'jinja2.ext.with_', 'hamlish_jinja.HamlishExtension']
    )

app = FlaskWithHamlish(__name__)
app.secret_key = secret_key
app.config['TEMPLATE_FOLDER'] = TEMPLATE_FOLDER
app.jinja_env.hamlish_mode = 'indented'
app.jinja_env.hamlish_enable_div_shortcut = True

# routs
app.add_url_rule('/',
                 view_func=Index.as_view('index'),
                 methods=['GET', 'POST'])
app.add_url_rule('/search',
                 view_func=Search.as_view('search'),
                 methods=['POST'])
app.add_url_rule('/signup',
                 view_func=SignUp.as_view('signup'),
                 methods=['GET', 'POST'])
app.add_url_rule('/login',
                 view_func=LogIn.as_view('login'),
                 methods=['GET', 'POST'])
app.add_url_rule('/addauthor',
                 view_func=AddAuthor.as_view('add_author'),
                 methods=['GET', 'POST'])
app.add_url_rule('/addbook',
                 view_func=AddBook.as_view('add_book'),
                 methods=['GET', 'POST'])
app.add_url_rule('/editbook/<title>',
                 view_func=EditBook.as_view('edit_book'),
                 methods=['GET', 'POST'])
app.add_url_rule('/editauthor/<name>',
                 view_func=EditAuthor.as_view('edit_author'),
                 methods=['GET', 'POST'])
app.add_url_rule('/author/<name>/remove',
                 view_func=RemoveAuthor.as_view('remove_author'),
                 methods=['GET'])
app.add_url_rule('/book/<title>/remove',
                 view_func=RemoveBook.as_view('remove_book'),
                 methods=['GET'])

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.haml'), 404


if __name__ == '__main__':
    build_db()
    app.run(host='0.0.0.0')