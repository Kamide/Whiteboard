from datetime import datetime
from decimal import Decimal
from flask_login import LoginManager, UserMixin
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from whiteboard import settings as wbs

db = SQLAlchemy()
migrate = Migrate(compare_type=True)
login_manager = LoginManager()
login_manager.login_view = 'auth.login'


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

    def __str__(self):
        return f'{self.display_name or self.full_name} @{self.username}'

    @property
    def is_active(self):
        return self.join_date is not None

    @property
    def is_teacher(self):
        return self.teacher is not None

    @property
    def is_student(self):
        return self.student is not None

    @property
    def identity(self):
        return 'Teacher' if self.is_teacher else 'Student'

    @property
    def classes(self):
        if self.is_teacher:
            return Class.query.filter_by(teacher_id=self.id)
        else:
            return Class.query.join(Enrollment).filter_by(student_id=self.id)


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
    absences = db.relationship('Absence', backref='student', cascade='all, delete')

    def __str__(self):
        return str(self.user)

    def absent(self, class_id, date=datetime.utcnow().date()):
        return Absence.query.filter_by(student_id=self.user_id, class_id=class_id, date=date).first()


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
    department_id = db.Column(db.Integer, db.ForeignKey('Departments.id', ondelete='CASCADE'), nullable=False)
    code = db.Column(db.String(wbs.COURSE_CODE_LEN))
    name = db.Column(db.String(255), nullable=False)

    __table_args__ = (db.UniqueConstraint('department_id', 'code'), )
    classes = db.relationship('Class', backref='course', cascade='all, delete')

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
    teacher_id = db.Column(db.Integer, db.ForeignKey('Teachers.user_id', ondelete='CASCADE'), nullable=False)
    term_id = db.Column(db.Integer, db.ForeignKey('Terms.id', ondelete='CASCADE'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('Courses.id', ondelete='CASCADE'), nullable=False)
    section = db.Column(db.String(wbs.CLASS_SECTION_LEN), nullable=False)
    schedule = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(255), nullable=False)

    __table_args__ = (db.UniqueConstraint('term_id', 'course_id', 'section'), )
    enrollments = db.relationship('Enrollment', backref='class_', cascade='all, delete')
    absences = db.relationship('Absence', backref='class_', cascade='all, delete')
    assignment_types = db.relationship('AssignmentType', backref='class_', cascade='all, delete')
    assignments = db.relationship('Assignment', backref='class_', cascade='all, delete')

    def __str__(self):
        return f'{self.term} {self.course}-{self.section}'

    def has_student(self, user):
        return Enrollment.query.filter_by(student_id=user.id, class_id=self.id).first()

    def has_user(self, user):
        if user.is_teacher:
            return self.teacher_id == user.id
        else:
            return self.has_student(user)


class Enrollment(db.Model):
    __tablename__ = 'Enrollments'
    student_id = db.Column(db.Integer, db.ForeignKey('Students.user_id', ondelete='CASCADE'))
    class_id = db.Column(db.Integer, db.ForeignKey('Classes.id', ondelete='CASCADE'))

    __table_args__ = (db.PrimaryKeyConstraint('student_id', 'class_id'), )

    def __str__(self):
        return f'{self.class_}—{self.student}'


class Absence(db.Model):
    __tablename__ = 'Absences'
    student_id = db.Column(db.Integer, db.ForeignKey('Students.user_id', ondelete='CASCADE'))
    class_id = db.Column(db.Integer, db.ForeignKey('Classes.id', ondelete='CASCADE'))
    date = db.Column(db.Date())

    __table_args__ = (db.PrimaryKeyConstraint('student_id', 'class_id', 'date'), )

    def __str__(self):
        return f'{self.class_}—{self.student}: Absent on {self.date}'


class AssignmentType(db.Model):
    __tablename__ = 'AssignmentTypes'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    class_id = db.Column(db.Integer, db.ForeignKey('Classes.id', ondelete='CASCADE'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    weight = db.Column(db.Integer, nullable=False)

    __table_args__ = (db.UniqueConstraint('class_id', 'name'),
                      db.CheckConstraint('weight > 0', 'CC_Weight'))
    assignments = db.relationship('Assignment', backref='assignmenttype', cascade='all, delete')

    def __repr__(self):
        return f'{self.class_}—{self.name} (Weight: {self.weight})'

    def __str__(self):
        return f'{self.name}: {round(self.actual_weight, 2):.3g}%'

    def collective_weight(self):
        return db.session.query(db.func.sum(AssignmentType.weight)).filter_by(class_id=self.class_id).scalar()

    @property
    def actual_weight(self):
        return self.weight * 100 / self.collective_weight()

    @property
    def count(self):
        return len(self.assignments)


class Assignment(db.Model):
    __tablename__ = 'Assignments'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    class_id = db.Column(db.Integer, db.ForeignKey('Classes.id', ondelete='CASCADE'), nullable=False)
    assignmenttype_id = db.Column(db.ForeignKey('AssignmentTypes.id', ondelete='CASCADE'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    weight_numerator = db.Column(db.Integer, nullable=False)
    weight_denominator = db.Column(db.Integer, nullable=False)
    due_date = db.Column(db.Date(), nullable=False)
    description = db.Column(db.String(255))

    __table_args__ = (db.UniqueConstraint('class_id', 'assignmenttype_id', 'name'),
                      db.CheckConstraint('weight_numerator > 0 AND weight_numerator < 101 AND weight_denominator > 0 AND weight_denominator < 101', name='CC_Weight'))

    def __repr__(self):
        return f'{self.class_}—{self.name}: Due on {self.due_date}'

    def __str__(self):
        return f'{self.name} (Due on {self.due_date})'

    @property
    def weight(self):
        return '%.2g' % round(self.weight_numerator / self.weight_denominator, 3)
