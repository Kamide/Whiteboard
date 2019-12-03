from flask import Blueprint, flash, redirect, render_template, url_for
from whiteboard import settings as wbs
from whiteboard.forms import CourseForm, DepartmentForm, MajorForm, TermForm
from whiteboard.models import Course, Department, Major, Term, db
from whiteboard.views import admin_required
from whiteboard.views.exceptions import EntityNotFound

academics = Blueprint('academics', __name__, template_folder='../templates/academics', url_prefix='/academics')


@academics.route('/')
def index():
    departments = Department.query.all()
    majors = Major.query.all()
    courses = Course.query.all()
    terms = Term.query.all()
    return render_template('academics.html', departments=departments, majors=majors, courses=courses, terms=terms)


@academics.route('/departments/new', methods=['GET', 'POST'])
@admin_required
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
            return redirect(url_for('academics.index'))

    return render_template('edit-form.html', title='Departments', card_title='New Department', form=form)


@academics.route('/departments/edit/<department_id>', methods=['GET', 'POST'])
@admin_required
def edit_department(department_id):
    department = Department.query.filter_by(id=department_id).first()

    if not department:
        raise EntityNotFound(entity_name=Department.__name__, entity_id=department_id)

    form = DepartmentForm(obj=department)

    if form.validate_on_submit():
        candidate = Department.query.filter(Department.name.ilike(form.name.data)).first()

        if candidate and candidate != department:
            flash('A department with that name already exists.')
        else:
            form.populate_obj(department)
            db.session.commit()
            flash(f'Changes to department #{department.id} have been made.', 'success')

    return render_template('edit-form.html', title='Departments', card_title=f'Editing Department #{department.id}: {department}', form=form)


@academics.route('/majors/new', methods=['GET', 'POST'])
@admin_required
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
            return redirect(url_for('academics.index'))

    return render_template('edit-form.html', title='Majors', card_title='New Major', form=form)


@academics.route('/majors/edit/<major_id>', methods=['GET', 'POST'])
@admin_required
def edit_major(major_id):
    major = Major.query.filter_by(id=major_id).first()

    if not major:
        raise EntityNotFound(entity_name=Major.__name__, entity_id=major_id)

    form = MajorForm(obj=major)

    if form.validate_on_submit():
        candidate = Major.query.filter(Major.name.ilike(form.name.data)).first()

        if candidate and candidate != major:
            flash('A major with that name already exists.')
        else:
            form.populate_obj(major)
            db.session.commit()
            flash(f'Changes to major #{major.id} have been made.', 'success')

    return render_template('edit-form.html', title='Majors', card_title=f'Editing Major #{major.id}: {major}', form=form)


@academics.route('/courses/new', methods=['GET', 'POST'])
@admin_required
def new_course():
    if Department.query.count() < 1:
        flash('Please add a department first before adding a course.')
        return redirect(url_for('academics.index'))

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
            return redirect(url_for('academics.index'))

    return render_template('edit-form.html', title='Courses', card_title='New Course', form=form)


@academics.route('/courses/edit/<course_id>', methods=['GET', 'POST'])
@admin_required
def edit_course(course_id):
    course = Course.query.filter_by(id=course_id).first()

    if not course:
        raise EntityNotFound(entity_name=Course.__name__, entity_id=course_id)

    form = CourseForm(obj=course)

    if form.validate_on_submit():
        candidate = Course.query.filter_by(department_id=form.department.data.id, code=form.code.data).first()

        if candidate and candidate != course:
            flash('A course with that code already exists.')
        else:
            form.populate_obj(course)
            db.session.commit()
            flash(f'Changes to course #{course.id} have been made.', 'success')

    return render_template('edit-form.html', title='Courses', card_title=f'Editing Course #{course.id}: {course}', form=form)


@academics.route('/terms/new', methods=['GET', 'POST'])
@admin_required
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
            return redirect(url_for('academics.index'))

    return render_template('edit-form.html', title=wbs.ACADEMIC_TERM.system_plural_capital, card_title=f'New {wbs.ACADEMIC_TERM.system_capital}', form=form)


@academics.route('/terms/edit/<term_id>', methods=['GET', 'POST'])
@admin_required
def edit_term(term_id):
    term = Term.query.filter_by(id=term_id).first()

    if not term:
        raise EntityNotFound(entity_name=wbs.ACADEMIC_TERM.system_capital, entity_id=term_id)

    form = TermForm(obj=term)

    if form.validate_on_submit():
        candidate = Term.query.filter((Term.start_date <= form.end_date.data) & (Term.end_date >= form.start_date.data)).first()

        if candidate and candidate != term:
            flash(f'A {wbs.ACADEMIC_TERM.system} within that date range already exists.')
        else:
            form.populate_obj(term)
            db.session.commit()
            flash(f'Changes to {wbs.ACADEMIC_TERM.system} #{term.id} have been made.', 'success')

    return render_template('edit-form.html', title=wbs.ACADEMIC_TERM.system_plural_capital, card_title=f'Editing {wbs.ACADEMIC_TERM.system_capital} #{term.id}: {term}', form=form)
