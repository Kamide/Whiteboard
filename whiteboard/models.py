from flask_login import LoginManager, UserMixin
from flask_sqlalchemy import SQLAlchemy
from whiteboard import settings as wbs

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'users.login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(wbs.CAMPUS_CARD.max_len), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(255), nullable=False)
    display_name = db.Column(db.String(255))
    email = db.Column(db.String(254), nullable=False, unique=True)
    join_date = db.Column(db.DateTime())

    teacher = db.relationship('Teacher', uselist=False, backref='user', cascade='all, delete')
    student = db.relationship('Student', uselist=False, backref='user', cascade='all, delete')

    @property
    def is_active(self):
        return self.join_date is not None

    @property
    def is_teacher(self):
        return self.teacher is not None

    @property
    def identity(self):
        return 'Teacher' if self.is_teacher else 'Student'

    def __str__(self):
        return f'{self.display_name or self.full_name} @{self.username}'


class Teacher(db.Model):
    __tablename__ = 'Teachers'
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id', ondelete='CASCADE'), primary_key=True)
    department_id = db.Column(db.Integer, db.ForeignKey('Departments.id', ondelete='SET NULL'))
    office = db.Column(db.String(255))
    office_hours = db.Column(db.String(255))

    classes = db.relationship('Class', backref='teacher', cascade='all, delete')

    def __str__(self):
        return str(self.user)


class Student(db.Model):
    __tablename__ = 'Students'
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id', ondelete='CASCADE'), primary_key=True)
    major_id = db.Column(db.Integer, db.ForeignKey('Majors.id', ondelete='SET NULL'))

    enrollments = db.relationship('Enrollment', backref='student', cascade='all, delete')

    def __str__(self):
        return str(self.user)


class Department(db.Model):
    __tablename__ = 'Departments'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    abbreviation = db.Column(db.String(wbs.DEPT_ABBREV_LEN), nullable=False, unique=True)
    chair = db.Column(db.String(255), nullable=False)
    office = db.Column(db.String(255), nullable=False)

    teachers = db.relationship('Teacher', backref='department')
    majors = db.relationship('Major', backref='department')
    courses = db.relationship('Course', backref='department', cascade='all, delete')

    def __str__(self):
        return f'{self.name} ({self.abbreviation})'


class Major(db.Model):
    __tablename__ = 'Majors'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    department_id = db.Column(db.Integer, db.ForeignKey('Departments.id', ondelete='SET NULL'))

    students = db.relationship('Student', backref='major')

    def __str__(self):
        return self.name


class Course(db.Model):
    __tablename__ = 'Courses'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    department_id = db.Column(db.Integer, db.ForeignKey('Departments.id', ondelete='CASCADE'))
    code = db.Column(db.String(wbs.COURSE_CODE_LEN))
    name = db.Column(db.String(255), nullable=False)

    classes = db.relationship('Class', backref='course', cascade='all, delete')
    __table_args__ = (db.UniqueConstraint('department_id', 'code'), )

    def __str__(self):
        return f'{self.department.abbreviation} {self.code}'


class Term(db.Model):
    __tablename__ = 'Terms'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    start_date = db.Column(db.Date(), nullable=False, unique=True)
    end_date = db.Column(db.Date(), nullable=False, unique=True)

    classes = db.relationship('Class', backref='term', cascade='all, delete')

    def __str__(self):
        return f'{self.name} {self.start_date.year}'


class Class(db.Model):
    __tablename__ = 'Classes'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('Teachers.user_id', ondelete='CASCADE'))
    term_id = db.Column(db.Integer, db.ForeignKey('Terms.id', ondelete='CASCADE'))
    course_id = db.Column(db.Integer, db.ForeignKey('Courses.id', ondelete='CASCADE'))
    section = db.Column(db.String(wbs.CLASS_SECTION_LEN), nullable=False)
    schedule = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(255), nullable=False)

    enrollments = db.relationship('Enrollment', backref='class_', cascade='all, delete')
    __table_args__ = (db.UniqueConstraint('term_id', 'course_id', 'section'), )

    def __str__(self):
        return f'{self.term} {self.course}-{self.section}'


class Enrollment(db.Model):
    __tablename__ = 'Enrollments'
    student_id = db.Column(db.Integer, db.ForeignKey('Students.user_id', ondelete='CASCADE'), primary_key=True)
    class_id = db.Column(db.Integer, db.ForeignKey('Classes.id', ondelete='CASCADE'), primary_key=True)

    def __str__(self):
        return f'{self.student}—{self.class_}'
