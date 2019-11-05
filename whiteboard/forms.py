from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class BaseRegistrationForm(FlaskForm):
    username = StringField('Academic ID', validators=[DataRequired()])
    full_name = StringField('Full Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])

class StudentRegistrationForm(BaseRegistrationForm):
    submit = SubmitField('Submit Application')

class TeacherRegistrationForm(BaseRegistrationForm):
    secret_pin = PasswordField('Secret PIN', validators=[DataRequired()])
    submit = SubmitField('Create Account')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')
