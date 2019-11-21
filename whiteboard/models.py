from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
from whiteboard.settings import CAMPUS_CARD, DEPT_ABBREV_LEN, COURSE_CODE_LEN

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Department(db.Model):
    __tablename__ = 'Departments'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    abbreviation = db.Column(db.String(DEPT_ABBREV_LEN), nullable=False, unique=True)
    chair = db.Column(db.String(255), nullable=False)
    office = db.Column(db.String(255), nullable=False)

    majors = db.relationship('Major', backref='department')
    courses = db.relationship('Course', backref='department', cascade='all, delete')
    teachers = db.relationship('Teacher', backref='department')

    def __str__(self):
        return f'{self.name} ({self.abbreviation})'


class Major(db.Model):
    __tablename__ = 'Majors'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    department_id = db.Column(db.Integer, db.ForeignKey('Departments.id', ondelete='SET NULL'))

    students = db.relationship('Student', backref='major')


class User(db.Model, UserMixin):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(CAMPUS_CARD.max_len), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(255), nullable=False)
    display_name = db.Column(db.String(255))
    email = db.Column(db.String(254), nullable=False, unique=True)
    join_date = db.Column(db.DateTime())

    teacher = db.relationship('Teacher', backref='user', cascade='all, delete')
    student = db.relationship('Student', backref='user', cascade='all, delete')

    @property
    def is_active(self):
        return self.join_date is not None

    @property
    def is_teacher(self):
        return self.teacher is not None


class Teacher(db.Model):
    __tablename__ = 'Teachers'
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id', ondelete='CASCADE'), primary_key=True)
    department_id = db.Column(db.Integer, db.ForeignKey('Departments.id', ondelete='SET NULL'))
    office = db.Column(db.String(255))
    office_hours = db.Column(db.String(255))


class Student(db.Model):
    __tablename__ = 'Students'
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id', ondelete='CASCADE'), primary_key=True)
    major_id = db.Column(db.Integer, db.ForeignKey('Majors.id', ondelete='SET NULL'))


class Course(db.Model):
    __tablename__ = 'Courses'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    department_id = db.Column(db.Integer, db.ForeignKey('Departments.id', ondelete='CASCADE'))
    code = db.Column(db.String(COURSE_CODE_LEN))
    name = db.Column(db.String(255), nullable=False)

    __table_args__ = (db.UniqueConstraint('department_id', 'code'), )


class Class(db.Model):
    __tablename__ = 'Classes'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    course_id = db.Column(db.Integer, db.ForeignKey('Courses.id', ondelete='CASCADE'))
    section = db.Column(db.String(4), nullable=False)
    start_date = db.Column(db.Date(), nullable=False)
    end_date = db.Column(db.Date(), nullable=False)
    location = db.Column(db.String(255), nullable=False)
    instructor = db.Column(db.Integer, db.ForeignKey('Teachers.user_id', ondelete='CASCADE'))
