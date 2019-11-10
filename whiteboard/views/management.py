from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from whiteboard.models import db, User
from whiteboard.settings import CAMPUS_CARD

management = Blueprint('management', __name__, template_folder='../templates/management', url_prefix='/management')


@management.before_request
@login_required
def restrict_management_to_teachers():
    if not current_user.is_teacher:
        abort(403)


@management.route('/')
def index():
    return render_template('management.html')


@management.route('/applicants', methods=['GET', 'POST'])
def applicants():
    applicants = User.query.filter_by(join_date=None)
    return render_template('applicants.html', applicants=applicants)


@management.route('/applicants/<applicant_id>', methods=['POST'])
def admissions(applicant_id):
    applicant = User.query.filter_by(id=applicant_id).first()

    if not applicant or applicant.is_active:
        flash('This applicant does not exist.', 'error')
        return redirect(url_for('management.applicants'))

    if 'decision' in request.form:
        pass
    elif 'confirmation' in request.form:
        if request.form['confirmation'] == 'Accept':
            applicant.join_date = datetime.utcnow()
            db.session.commit()
            flash(f"{applicant.full_name}'s account with {CAMPUS_CARD.formal_name} {applicant.username} has been successfully verified.", 'success')
        elif request.form['confirmation'] == 'Reject':
            db.session.delete(applicant)
            db.session.commit()
            flash(f"{applicant.full_name}'s application with {CAMPUS_CARD.formal_name} {applicant.username} has been successfully deleted.", 'success')

        return redirect(url_for('management.applicants'))
    else:
        flash('An unknown error has occurred', 'error')
        return redirect(url_for('management.applicants'))

    return render_template('admissions.html', applicant=applicant)
