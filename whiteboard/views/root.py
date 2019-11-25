from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required
from whiteboard.models import User, Department, Major, Course, Term, Class

root = Blueprint('root', __name__, template_folder='../templates/root')


@root.route('/')
@root.route('/index')
def index():
    return render_template('index.html')


@root.route('/users')
@login_required
def users():
    active_users = User.query.filter(User.join_date != None)
    teachers = active_users.filter(User.teacher != None)
    students = active_users.filter(User.student != None)
    return render_template('users.html', teachers=teachers, students=students)


@root.route('/academics')
def academics():
    departments = Department.query.all()
    majors = Major.query.all()
    courses = Course.query.all()
    terms = Term.query.all()
    return render_template('academics.html', departments=departments, majors=majors, courses=courses, terms=terms)


@root.route('/classes')
@login_required
def classes():
    classes = Class.query.all()
    return render_template('classes.html', classes=classes)


@root.route('/classes/<class_id>')
@login_required
def class_info(class_id):
    current_class = Class.query.filter_by(id=class_id).first()

    if not current_class:
        flash('This class does not exist!')
        return redirect(url_for('root.classes'))

    return render_template('class.html', current_class=current_class)
