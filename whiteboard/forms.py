from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import InputRequired, Regexp, Length, Email, EqualTo
from whiteboard.settings import CAMPUS_CARD


class RegistrationForm(FlaskForm):
    username = StringField(f'Username ({CAMPUS_CARD})', validators=[InputRequired(), Regexp('^[^\\W_]+$', message=f'Username is restricted to word characters; check your campus card for help.'), Length(min=CAMPUS_CARD.min_len, max=CAMPUS_CARD.max_len)])
    full_name = StringField('Full Name', validators=[InputRequired(), Length(max=255)])
    display_name = StringField('Display Name', validators=[Length(max=255)])
    email = StringField('Email', validators=[InputRequired(), Email(), Length(max=254)])
    password = PasswordField('Password', validators=[InputRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('password')])
    is_fs_member = BooleanField('Part of Faculty or Staff?')
    submit = SubmitField('Submit Application')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Log In')
