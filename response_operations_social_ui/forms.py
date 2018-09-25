import logging

from flask_wtf import FlaskForm
from structlog import wrap_logger
from wtforms import PasswordField, StringField, \
    SubmitField
from wtforms.validators import InputRequired

logger = wrap_logger(logging.getLogger(__name__))


class LoginForm(FlaskForm):
    username = StringField('Username', [InputRequired("Please enter a username")])
    password = PasswordField('Password', [InputRequired("Please enter a password")])
    submit = SubmitField('Sign in')


class SearchForm(FlaskForm):
    query = StringField('Query')
    submit = SubmitField('Search')


class ChangeGroupStatusForm(FlaskForm):
    event = StringField('event')
    submit = SubmitField('Confirm')
