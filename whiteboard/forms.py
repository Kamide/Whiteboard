from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import Email, EqualTo, InputRequired, Length, Regexp
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from whiteboard.models import Department
from whiteboard.settings import CAMPUS_CARD, DEPT_ABBREV_LEN, COURSE_CODE_LEN


class RegistrationForm(FlaskForm):
    username = StringField(f'Username ({CAMPUS_CARD})', validators=[InputRequired(), Length(min=CAMPUS_CARD.min_len, max=CAMPUS_CARD.max_len), Regexp('^[^\\W_]+$', message=f'Username is restricted to word characters; check your campus card for help.')])
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
    abbreviation = StringField(f'Abbreviation (No Longer than {DEPT_ABBREV_LEN} Characters)', validators=[InputRequired(), Length(min=1, max=4), Regexp('^[^\\W_]+$', message='Abbreviation is restricted to word characters, i.e. no spaces.')])
    chair = StringField('Chair', validators=[InputRequired()])
    office = StringField('Office', validators=[InputRequired()])
    submit = SubmitField('Submit')


def department_query():
    return Department.query


class MajorForm(FlaskForm):
    name = StringField('Name')
    department = QuerySelectField('Department', query_factory=department_query, allow_blank=True)
    submit = SubmitField('Submit')


class CourseForm(FlaskForm):
    department = QuerySelectField('Department (Course Prefix)', query_factory=department_query, allow_blank=False)
    code = StringField(f'Course Number (No Longer than {COURSE_CODE_LEN} Characters)', validators=[InputRequired(), Length(min=1, max=COURSE_CODE_LEN), Regexp('[0-9]+$', message='Course number must only contain digits.')])
    name = StringField(f'Name')
    submit = SubmitField('Submit')
