from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from whiteboard.forms import DepartmentForm, MajorForm, CourseForm
from whiteboard.models import db, User, Department, Major, Course
from whiteboard.settings import CAMPUS_CARD

admin = Blueprint('admin', __name__, template_folder='../templates/admin')


@admin.before_request
@login_required
def admin_required():
    if not current_user.is_teacher:
        abort(403)


@admin.route('/applicants', methods=['GET', 'POST'])
def applicants():
    applicants = User.query.filter_by(join_date=None)
    return render_template('applicants.html', applicants=applicants)


@admin.route('/applicants/<applicant_id>', methods=['POST'])
def admissions(applicant_id):
    applicant = User.query.filter_by(id=applicant_id).first()

    if not applicant or applicant.is_active:
        flash('This applicant does not exist.', 'error')
        return redirect(url_for('admin.applicants'))

    if 'decision' in request.form:
        pass
    elif 'confirmation' in request.form:
        if request.form['confirmation'] == 'Accept':
            applicant.join_date = datetime.utcnow()
            db.session.commit()
            flash(f"{applicant.full_name}'s account with {CAMPUS_CARD.formal_name} {applicant.username} has been verified.", 'success')
        elif request.form['confirmation'] == 'Reject':
            db.session.delete(applicant)
            db.session.commit()
            flash(f"{applicant.full_name}'s application with {CAMPUS_CARD.formal_name} {applicant.username} has been deleted.", 'success')

        return redirect(url_for('admin.applicants'))
    else:
        flash('An unknown error has occurred', 'error')
        return redirect(url_for('admin.applicants'))

    return render_template('admissions.html', applicant=applicant)


@admin.route('/academics/departments/new', methods=['GET', 'POST'])
def new_department():
    form = DepartmentForm()

    if form.validate_on_submit():
        candidate = Department.query.filter(Department.name.ilike(form.name.data)).first()

        if candidate:
            flash('A department with that name already exists.', 'error')
        else:
            department = Department()
            form.populate_obj(department)
            db.session.add(department)
            db.session.commit()
            flash(f'{department.name} has been created.', 'success')
            return redirect(url_for('root.academics'))

    return render_template('division.html', title='Departments', card_title='New Department', form=form)


@admin.route('/academics/departments/edit/<department_id>', methods=['GET', 'POST'])
def edit_department(department_id):
    department = Department.query.filter_by(id=department_id).first()

    if not department:
        flash('This department does not exist.', 'error')
        return redirect(url_for('root.academics'))

    form = DepartmentForm(obj=department)

    if form.validate_on_submit():
        candidate = Department.query.filter(Department.name.ilike(form.name.data)).first()

        if candidate and candidate != department:
            flash('A department with that name already exists.')
        else:
            form.populate_obj(department)
            db.session.commit()
            flash(f'Changes to department #{department.id} have been made.', 'success')

    return render_template('division.html', title='Departments', card_title=f'Editing "{department.name}"', form=form)


@admin.route('/academics/majors/new', methods=['GET', 'POST'])
def new_major():
    form = MajorForm()

    if form.validate_on_submit():
        candidate = Major.query.filter(Major.name.ilike(form.name.data)).first()

        if candidate:
            flash('A department with that name already exists.', 'error')
        else:
            major = Major()
            form.populate_obj(major)
            db.session.add(major)
            db.session.commit()
            flash(f'{major.name} has been created.', 'success')
            return redirect(url_for('root.academics'))

    return render_template('division.html', title='Majors', card_title='New Major', form=form)


@admin.route('/academics/majors/edit/<major_id>', methods=['GET', 'POST'])
def edit_major(major_id):
    major = Major.query.filter_by(id=major_id).first()

    if not major:
        flash('This major does not exist.', 'error')
        return redirect(url_for('root.academics'))

    form = MajorForm(obj=major)

    if form.validate_on_submit():
        candidate = Major.query.filter(Major.name.ilike(form.name.data)).first()

        if candidate and candidate != major:
            flash('A major with that name already exists.')
        else:
            form.populate_obj(major)
            db.session.commit()
            flash(f'Changes to major #{major.id} have been made.', 'success')

    return render_template('division.html', title='Majors', card_title=f'Editing "{major.name}"', form=form)


@admin.route('/academics/courses/new', methods=['GET', 'POST'])
def new_course():
    form = CourseForm()

    if form.validate_on_submit():
        candidate = Course.query.filter_by(department_id=form.department.data.id, code=form.code.data).first()

        if candidate:
            flash('A course with that code already exists.', 'error')
        else:
            course = Course()
            form.populate_obj(course)
            db.session.add(course)
            db.session.commit()
            flash(f'{course.department.abbreviation} {course.code} ({course.name}) has been created.', 'success')
            return redirect(url_for('root.academics'))

    return render_template('division.html', title='Courses', card_title='New Course', form=form)


@admin.route('/academics/courses/edit/<course_id>', methods=['GET', 'POST'])
def edit_course(course_id):
    course = Course.query.filter_by(id=course_id).first()

    if not course:
        flash('This course does not exist.', 'error')
        return redirect(url_for('root.academics'))

    form = CourseForm(obj=course)

    if form.validate_on_submit():
        candidate = Course.query.filter_by(department_id=form.department.data.id, code=form.code.data).first()

        if candidate and candidate != course:
            flash('A course with that code already exists.')
        else:
            form.populate_obj(course)
            db.session.commit()
            flash(f'Changes to course #{course.id} have been made.', 'success')

    return render_template('division.html', title='Courses', card_title=f'Editing "{course.name}"', form=form)
