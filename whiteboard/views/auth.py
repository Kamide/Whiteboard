from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from whiteboard.forms import RegistrationForm, LoginForm
from whiteboard.models import db, User

auth = Blueprint('auth', __name__, template_folder='../templates/auth')


@auth.route('/register', methods=['GET', 'POST'])
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
            db.session.commit()
            flash(f"{form.username.data}'s application has been sent for verification.", 'success')
            return redirect(url_for('root.index'))
    return render_template('register.html', title='Register', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            if user.is_active:
                login_user(user)
                return redirect(url_for('root.index'))
            else:
                flash('Your account application is currently being processed. For more information, please refer to a faculty or staff member.')
        else:
            flash('You have entered an invalid username or password.', 'error')
    return render_template('login.html', title='Log In', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('logout.html')
