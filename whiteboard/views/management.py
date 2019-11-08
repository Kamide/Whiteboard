from flask import Blueprint, render_template, abort
from flask_login import login_required, current_user
from whiteboard.models import User

management = Blueprint('management', __name__, template_folder='../templates/management')


@management.before_request
@login_required
def restrict_management_to_teachers():
    if not current_user.is_teacher:
        abort(403)


@management.route('/applications')
def applications():
    applicants = User.query.filter_by(join_date=None)
    return render_template('applications.html', title='Applications', applicants=applicants)
