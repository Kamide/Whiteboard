from datetime import datetime
from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from whiteboard import settings as wbs
from whiteboard.forms import LoginForm, RegistrationForm
from whiteboard.models import Student, Teacher, User, db
from whiteboard.views import admin_required, anonymous_required

auth = Blueprint('auth', __name__, template_folder='../templates/auth')


@auth.route('/register', methods=['GET', 'POST'])
@anonymous_required
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first():
            flash('This username is already in use.', 'error')
        elif User.query.filter_by(email=form.email.data).first():
            flash('This email is already in use.', 'error')
        else:
            new_user = User(username=form.username.data.upper(), password=generate_password_hash(form.password.data), full_name=form.full_name.data, display_name=form.display_name.data, email=form.email.data.lower())
            db.session.add(new_user)
            db.session.flush()

            if form.is_teacher.data:
                new_teacher = Teacher(user_id=new_user.id)
                db.session.add(new_teacher)
            else:
                new_student = Student(user_id=new_user.id)
                db.session.add(new_student)

            db.session.commit()
            flash(f"{form.username.data}'s application has been sent for verification.", 'success')
            return redirect(url_for('root.index'))

    return render_template('register.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
@anonymous_required
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data.upper()).first()

        if user and check_password_hash(user.password, form.password.data):
            if user.is_active:
                login_user(user)
                return redirect(url_for('root.index'))
            else:
                flash('Your account application is currently being processed. For more information, please refer to a faculty or staff member.')
        else:
            flash('You have entered an invalid username or password.', 'error')

    return render_template('login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been successfully logged out.', 'success')
    return redirect(url_for('root.index'))


@auth.route('/applicants', methods=['GET', 'POST'])
@admin_required
def applicants():
    applicants = User.query.filter_by(join_date=None)
    return render_template('applicants.html', applicants=applicants)


@auth.route('/applicants/<applicant_id>', methods=['POST'])
@admin_required
def admissions(applicant_id):
    applicant = User.query.filter_by(id=applicant_id).first()

    if not applicant or applicant.is_active:
        flash('This applicant does not exist.', 'error')
        return redirect(url_for('auth.applicants'))

    if 'decision' in request.form:
        pass
    elif 'confirmation' in request.form:
        if request.form['confirmation'] == 'Accept':
            applicant.join_date = datetime.utcnow()
            db.session.commit()
            flash(f"{applicant.full_name}'s account with {wbs.CAMPUS_CARD.formal_name} {applicant.username} has been verified.", 'success')
        elif request.form['confirmation'] == 'Reject':
            db.session.delete(applicant)
            db.session.commit()
            flash(f"{applicant.full_name}'s application with {wbs.CAMPUS_CARD.formal_name} {applicant.username} has been deleted.", 'success')

        return redirect(url_for('auth.applicants'))
    else:
        flash('An unknown error has occurred', 'error')
        return redirect(url_for('auth.applicants'))

    return render_template('admissions.html', applicant=applicant)


@auth.route('/users')
@login_required
def users():
    active_users = User.query.filter(User.join_date != None)
    teachers = active_users.filter(User.teacher != None)
    students = active_users.filter(User.student != None)
    return render_template('users.html', teachers=teachers, students=students)


@auth.route('/users/<user_id>')
@login_required
def user_info(user_id):
    user = User.query.filter_by(id=user_id).first()

    if not user:
        abort(404)

    return render_template('user.html', user=user)
