from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required
from whiteboard.forms import StudentRegistrationForm, TeacherRegistrationForm, LoginForm

auth = Blueprint('auth', __name__, template_folder='../templates/auth')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = StudentRegistrationForm()
    if form.validate_on_submit():
        flash(f'Account with username "{form.username.data}" has been sent for verification.', 'success')
        return redirect(url_for('root.index'))
    return render_template('register.html', title='Register', form=form)

@auth.route('/register/teacher', methods=['GET', 'POST'])
def register_teacher():
    form = TeacherRegistrationForm()
    if form.validate_on_submit():
        flash(f'Account with username "{form.username.data}" has been created.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html', title='Register', form=form, is_teacher=True)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect(url_for('root.index'))
    return render_template('login.html', title='Log In', form=form)


@auth.route('/logout')
@login_required
def logout():
    return render_template('logout.html')
