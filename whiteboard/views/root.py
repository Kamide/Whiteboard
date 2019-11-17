from flask import Blueprint, render_template
from whiteboard.models import Department, Major, User

root = Blueprint('root', __name__, template_folder='../templates/root')


@root.route('/')
@root.route('/index')
def index():
    return render_template('index.html')


@root.route('/academics')
def academics():
    departments = Department.query.all()
    majors = Major.query.all()
    return render_template('academics.html', departments=departments, majors=majors)


@root.route('/users')
def users():
    active_users = User.query.filter(User.join_date != None)
    teachers = active_users.filter(User.teacher != None)
    students = active_users.filter(User.student != None)
    return render_template('users.html', teachers=teachers, students=students)
