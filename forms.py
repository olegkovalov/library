from flask_wtf import Form
from wtforms import TextField, SubmitField, PasswordField, SelectField, validators
from wtforms.ext.sqlalchemy.fields import QuerySelectField
# from wtforms import HiddenField, SubmitField, TextField, IntegerField, TextAreaField, FileField, ValidationError, validators
# import re

req_msg = u'Field required'



class SignUpForm(Form):
    nickname = TextField( u'Nickname', [
        validators.Length(min=3, max=12),
        validators.Required(req_msg)
    ])
    password = PasswordField(u'Password', [
        validators.Length(min=6, max=32),
        validators.Required(req_msg),
        validators.EqualTo('confirm', message=u'Passwords must mutch')
    ])
    confirm = PasswordField(u'Repeat password')
    submit = SubmitField(u'Sign up')



class LogInForm(Form):
    nickname = TextField( u'Nickname', [
        validators.Length(min=3, max=12),
        validators.Required(req_msg)
    ])
    password = PasswordField(u'Password', [
        validators.Length(min=6, max=32),
        validators.Required(req_msg)
    ])
    submit = SubmitField(u'Log in')


class AddAuthorForm(Form):
    name = TextField(u'Name', [
        validators.Length(min=3, max=12),
        validators.required(req_msg)
    ])
    title = TextField(u'Title', [
        validators.Length(min=3, max=30),
        validators.required(req_msg)
    ])
    # book_id = SelectField(u'book', validators=[validators.Required()], coerce=int)
    # book_id = SelectField(u'book', coerce=int)
    submit = SubmitField(u'Add')



class AddBookForm(Form):
    title = TextField(u'Title', [
        validators.Length(min=3, max=30),
        validators.required(req_msg)
    ])
    name = TextField(u'Name', [
        validators.Length(min=3, max=30),
        validators.required(req_msg)
    ])
    submit = SubmitField(u'Add')



class EditBookForm(AddBookForm):
    submit = SubmitField(u'Eit')



class EditAuthorForm(AddBookForm):
    submit = SubmitField(u'Eit')
