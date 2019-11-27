from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from whiteboard.forms import EnrollmentForm
from whiteboard.models import db, User, Student, Department, Major, Course, Term, Class, Enrollment

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


@root.route('/users/<user_id>')
@login_required
def user_info(user_id):
    user = User.query.filter_by(id=user_id).first()

    if not user:
        abort(404)

    return render_template('user.html', user=user)


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


@root.route('/classes/<class_id>', methods=['GET', 'POST'])
@login_required
def class_info(class_id):
    current_class = Class.query.filter_by(id=class_id).first()

    if not current_class:
        flash('This class does not exist!', 'error')
        return redirect(url_for('root.classes'))

    students = Student.query.join(Enrollment).filter_by(class_id=class_id)

    if current_user.is_teacher:
        form = EnrollmentForm()

        if form.validate_on_submit():
            if request.method != 'POST' or not request.form['action']:
                abort(400)

            student = Student.query.filter_by(user_id=form.student.data.user_id).first()

            if student:
                student_enrolled = Enrollment.query.filter_by(student_id=student.user.id, class_id=class_id).first()

                if request.form['action'] == 'Enroll Student':
                    if student_enrolled:
                        flash('This student is already enrolled in this class.')
                    else:
                        enrollment = Enrollment(student_id=student.user.id, class_id=class_id)
                        db.session.add(enrollment)
                        db.session.commit()
                        flash(f'{student} has been enrolled.', 'success')
                else:
                    if student_enrolled:
                        db.session.delete(student_enrolled)
                        db.session.commit()
                        flash(f'{student} has been withdrawn from the class.', 'success')
                    else:
                        flash("You cannot withdraw a student that has not been enrolled.")
            else:
                flash('This student does not exist!', 'error')

        return render_template('class.html', current_class=current_class, students=students, form=form)

    return render_template('class.html', current_class=current_class, students=students)
