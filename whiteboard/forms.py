from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import Email, EqualTo, InputRequired, Length, Regexp
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from whiteboard.models import Department
from whiteboard.settings import CAMPUS_CARD


class RegistrationForm(FlaskForm):
    username = StringField(f'Username ({CAMPUS_CARD})', validators=[InputRequired(), Regexp('^[^\\W_]+$', message=f'Username is restricted to word characters; check your campus card for help.'), Length(min=CAMPUS_CARD.min_len, max=CAMPUS_CARD.max_len)])
    full_name = StringField('Full Name', validators=[InputRequired(), Length(max=255)])
    display_name = StringField('Display Name', validators=[Length(max=255)])
    email = StringField('Email', validators=[InputRequired(), Email(), Length(max=254)])
    password = PasswordField('Password', validators=[InputRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('password')])
    is_teacher = BooleanField('Part of Faculty or Staff?')
    submit = SubmitField('Submit Application')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Log In')


class DepartmentForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired()])
    chair = StringField('Chair', validators=[InputRequired()])
    office = StringField('Office', validators=[InputRequired()])


class NewDepartmentForm(DepartmentForm):
    submit = SubmitField('Add Department')


class EditDepartmentForm(DepartmentForm):
    submit = SubmitField('Apply Changes')


def department_query():
    return Department.query


class MajorForm(FlaskForm):
    name = StringField('Name')
    department = QuerySelectField('Department', query_factory=department_query, allow_blank=True)


class NewMajorForm(MajorForm):
    submit = SubmitField('Add Major')


class EditMajorForm(MajorForm):
    submit = SubmitField('Apply Changes')
