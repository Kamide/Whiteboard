from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.fields.html5 import DateField
from wtforms.validators import Email, EqualTo, InputRequired, Length, Regexp, ValidationError
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from whiteboard.models import User, Student, Department, Term, Course
from whiteboard import settings as wbs


def student_query():
    return Student.query.join(User).filter(User.join_date != None)


def department_query():
    return Department.query


def term_query():
    return Term.query


def course_query():
    return Course.query


class RegistrationForm(FlaskForm):
    username = StringField(f'Username ({wbs.CAMPUS_CARD})', validators=[InputRequired(), Length(min=wbs.CAMPUS_CARD.min_len, max=wbs.CAMPUS_CARD.max_len), Regexp('^[^\\W_]+$', message=f'Username is restricted to word characters; check your campus card for help.')])
    full_name = StringField('Full Name', validators=[InputRequired(), Length(max=255)])
    display_name = StringField('Display Name', validators=[Length(max=255)])
    email = StringField('Email', validators=[InputRequired(), Email(), Length(max=254)])
    password = PasswordField('Password', validators=[InputRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('password')])
    is_teacher = BooleanField('Part of Faculty or Staff?')
    submit = SubmitField('Submit Application')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=wbs.CAMPUS_CARD.min_len, max=wbs.CAMPUS_CARD.max_len)])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Log In')


class DepartmentForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired(), Length(max=255)])
    abbreviation = StringField(f'Abbreviation (No Longer than {wbs.DEPT_ABBREV_LEN} Characters)', validators=[InputRequired(), Length(max=4), Regexp('^[^\\W_]+$', message='Abbreviation is restricted to word characters, i.e. no spaces.')])
    chair = StringField('Chair', validators=[InputRequired(), Length(max=255)])
    office = StringField('Office', validators=[InputRequired(), Length(max=255)])
    submit = SubmitField('Submit')


class MajorForm(FlaskForm):
    name = StringField('Name')
    department = QuerySelectField('Department', query_factory=department_query, allow_blank=True)
    submit = SubmitField('Submit')


class CourseForm(FlaskForm):
    department = QuerySelectField('Department (Course Prefix)', query_factory=department_query, allow_blank=False)
    code = StringField(f'Course Number (No Longer than {wbs.COURSE_CODE_LEN} Characters)', validators=[InputRequired(), Length(max=wbs.COURSE_CODE_LEN), Regexp('[0-9]+$', message='Course number must only contain digits.')])
    name = StringField('Name', validators=[InputRequired(), Length(max=255)])
    submit = SubmitField('Submit')


class TermForm(FlaskForm):
    name = StringField(wbs.ACADEMIC_TERM.name_capital, validators=[InputRequired(), Length(max=255)])
    start_date = DateField('Start Date')
    end_date = DateField('End Date')
    submit = SubmitField('Submit')

    def validate_end_date(form, field):
        if field.data and form.start_date.data and field.data <= form.start_date.data:
            raise ValidationError('End date must be after start date.')


class ClassForm(FlaskForm):
    term = QuerySelectField(wbs.ACADEMIC_TERM.system_capital, query_factory=term_query, allow_blank=False)
    course = QuerySelectField('Course', query_factory=course_query, allow_blank=False)
    section = StringField(f'Section (No Longer than {wbs.CLASS_SECTION_LEN} Characters)', validators=[InputRequired(), Length(max=wbs.CLASS_SECTION_LEN),  Regexp('^[^\\W_]+$', message='Section is restricted to word characters, i.e. no spaces.')])
    schedule = StringField('Schedule', validators=[InputRequired(), Length(max=255)])
    location = StringField('Location', validators=[InputRequired(), Length(max=255)])
    submit = SubmitField('Submit')


class EnrollmentForm(FlaskForm):
    student = QuerySelectField('Student', query_factory=student_query, allow_blank=False)
