from functools import wraps
from flask import abort, redirect, url_for
from flask_login import current_user, login_required
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect()


def anonymous_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_anonymous:
            return f(*args, **kwargs)

        return redirect(url_for('auth.logout'))

    return decorated_function


def admin_required(f):
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if current_user.is_teacher:
            return f(*args, **kwargs)

        abort(403)

    return decorated_function
