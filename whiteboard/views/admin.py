from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from whiteboard.forms import DepartmentForm, MajorForm, CourseForm, TermForm, ClassForm
from whiteboard.models import db, User, Department, Major, Course, Term, Class
from whiteboard import settings as wbs

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
            flash(f"{applicant.full_name}'s account with {wbs.CAMPUS_CARD.formal_name} {applicant.username} has been verified.", 'success')
        elif request.form['confirmation'] == 'Reject':
            db.session.delete(applicant)
            db.session.commit()
            flash(f"{applicant.full_name}'s application with {wbs.CAMPUS_CARD.formal_name} {applicant.username} has been deleted.", 'success')

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
            flash(f'{department} has been created.', 'success')
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

    return render_template('division.html', title='Departments', card_title=f'Editing Department #{department.id}: {department}', form=form)


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
            flash(f'{major} has been created.', 'success')
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

    return render_template('division.html', title='Majors', card_title=f'Editing Major #{major.id}: {major}', form=form)


@admin.route('/academics/courses/new', methods=['GET', 'POST'])
def new_course():
    if Department.query.count() < 1:
        flash('Please add a department first before adding a course.')
        return redirect(url_for('root.academics'))

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
            flash(f'{course} has been created.', 'success')
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

    return render_template('division.html', title='Courses', card_title=f'Editing Course #{course.id}: {course}', form=form)


@admin.route('/terms/new', methods=['GET', 'POST'])
def new_term():
    form = TermForm()

    if form.validate_on_submit():
        candidate = Term.query.filter((Term.start_date <= form.end_date.data) & (Term.end_date >= form.start_date.data)).first()

        if candidate:
            flash(f'A {wbs.ACADEMIC_TERM.system} within that date range already exists.', 'error')
        else:
            term = Term()
            form.populate_obj(term)
            db.session.add(term)
            db.session.commit()
            flash(f'{term} has been created.', 'success')
            return redirect(url_for('root.academics'))

    return render_template('division.html', title=wbs.ACADEMIC_TERM.system_plural_capital, card_title=f'New {wbs.ACADEMIC_TERM.system_capital}', form=form)


@admin.route('/terms/edit/<term_id>', methods=['GET', 'POST'])
def edit_term(term_id):
    term = Term.query.filter_by(id=term_id).first()

    if not term:
        flash(f'This {wbs.ACADEMIC_TERM.system} does not exist.', 'error')
        return redirect(url_for('root.academics'))

    form = TermForm(obj=term)

    if form.validate_on_submit():
        candidate = Term.query.filter((Term.start_date <= form.end_date.data) & (Term.end_date >= form.start_date.data)).first()

        if candidate and candidate != term:
            flash(f'A {wbs.ACADEMIC_TERM.system} within that date range already exists.')
        else:
            form.populate_obj(term)
            db.session.commit()
            flash(f'Changes to {wbs.ACADEMIC_TERM.system} #{term.id} have been made.', 'success')

    return render_template('division.html', title=wbs.ACADEMIC_TERM.system_plural_capital, card_title=f'Editing {wbs.ACADEMIC_TERM.system_capital} #{term.id}: {term}', form=form)


@admin.route('/classes/new', methods=['GET', 'POST'])
def new_class():
    prereqs = []

    if Course.query.count() < 1:
        prereqs.append('course')

    if Term.query.count() < 1:
        prereqs.append(wbs.ACADEMIC_TERM.system)

    if prereqs:
        flash(f"Please add a {', '.join(prereqs)} first before adding a class.")
        return redirect(url_for('root.classes'))

    form = ClassForm()

    if form.validate_on_submit():
        candidate = Class.query.filter_by(term_id=form.term.data.id, course_id=form.course.data.id, section=form.section.data).first()

        if candidate:
            flash(f'A class with that {wbs.ACADEMIC_TERM.system}, course, and section already exists.', 'error')
        else:
            class_ = Class()
            form.populate_obj(class_)
            class_.teacher_id = current_user.id
            db.session.add(class_)
            db.session.commit()
            flash(f'{class_} has been created.', 'success')
            return redirect(url_for('root.classes'))

    return render_template('division.html', title='Classes', card_title='New Class', back_url='root.classes', form=form)


@admin.route('/classes/edit/<class_id>', methods=['GET', 'POST'])
def edit_class(class_id):
    class_ = Class.query.filter_by(id=class_id).first()

    if not class_:
        flash('This class does not exist.', 'error')
        return redirect(url_for('root.classes'))

    if class_.teacher.user != current_user:
        flash("You do not have permission to change another instructor's class.", 'error')
        return redirect(url_for('root.classes'))

    form = ClassForm(obj=class_)

    if form.validate_on_submit():
        candidate = Class.query.filter_by(term_id=form.term.data.id, course_id=form.course.data.id, section=form.section.data).first()

        if candidate and candidate != class_:
            flash(f'A class with that {wbs.ACADEMIC_TERM.system}, course, and section already exists.')
        else:
            form.populate_obj(class_)
            db.session.commit()
            flash(f'Changes to class #{class_.id} have been made.', 'success')

    return render_template('division.html', title='Classes', card_title=f'Editing Class #{class_.id}: {class_}', back_url='root.classes', form=form)
