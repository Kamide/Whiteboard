from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
from whiteboard.settings import CAMPUS_CARD

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Department(db.Model):
    __tablename__ = 'Departments'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    chair = db.Column(db.String(255), nullable=False)
    office = db.Column(db.String(255), nullable=False)


class Major(db.Model):
    __tablename__ = 'Majors'
    id = db.Column(db.Integer, primary_key=True)
    department_id = db.Column(db.Integer, db.ForeignKey('Departments.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)


class User(db.Model, UserMixin):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
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
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'), primary_key=True)
    department_id = db.Column(db.Integer, db.ForeignKey('Departments.id'))
    office = db.Column(db.String(255))
    office_hours = db.Column(db.String(255))


class Student(db.Model):
    __tablename__ = 'Students'
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'), primary_key=True)
    major_id = db.Column(db.Integer, db.ForeignKey('Majors.id'))
