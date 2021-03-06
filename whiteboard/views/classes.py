from datetime import datetime
from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from whiteboard import settings as wbs
from whiteboard.forms import AbsenceForm, ClassForm, EnrollmentForm
from whiteboard.models import Absence, Class, Course, Enrollment, Student, Term, db
from whiteboard.views import admin_required
from whiteboard.views.exceptions import EntityNotFound

classes = Blueprint('classes', __name__, template_folder='../templates/classes', url_prefix='/classes')


def verify_class_exists(class_id):
    current_class = Class.query.filter_by(id=class_id).first()

    if not current_class:
        raise EntityNotFound(entity_name=Class.__name__, entity_id=class_id)

    return current_class


def verify_user_teaches_class(class_id):
    current_class = verify_class_exists(class_id)

    if current_class.teacher.user != current_user:
        abort(403, "You do not have permission to change another instructor's class.")

    return current_class


def get_student_info(class_id, student_id, date=datetime.utcnow().date()):
    verify_user_teaches_class(class_id)
    student_enrollment = Enrollment.query.filter_by(student_id=student_id, class_id=class_id).first()

    if not student_enrollment:
        abort(400)

    student_absence = Absence.query.filter_by(student_id=student_id, class_id=class_id, date=date).first()
    return student_enrollment, student_absence


@classes.route('/')
@login_required
def index():
    classes = Class.query.all()
    return render_template('classes.html', classes=classes)


@classes.route('/new', methods=['GET', 'POST'])
@admin_required
def new_class():
    prereqs = []

    if Course.query.count() < 1:
        prereqs.append('course')

    if Term.query.count() < 1:
        prereqs.append(wbs.ACADEMIC_TERM.system)

    if prereqs:
        flash(f"Please add a {', '.join(prereqs)} first before adding a class.")
        return redirect(url_for('classes.index'))

    form = ClassForm()

    if form.validate_on_submit():
        candidate = Class.query.filter_by(term_id=form.term.data.id, course_id=form.course.data.id).filter(Class.section.ilike(form.section.data)).first()

        if candidate:
            flash(f'A class with that {wbs.ACADEMIC_TERM.system}, course, and section already exists.', 'error')
        else:
            class_ = Class(teacher_id=current_user.id)
            form.populate_obj(class_)
            db.session.add(class_)
            db.session.commit()
            flash(f'{class_} has been created.', 'success')
            return redirect(url_for('classes.index'))

    return render_template('edit-form.html', title='Classes', card_title='New Class', form=form)


@classes.route('/edit/<class_id>', methods=['GET', 'POST'])
@admin_required
def edit_class(class_id):
    class_ = verify_user_teaches_class(class_id)
    form = ClassForm(obj=class_)

    if form.validate_on_submit():
        candidate = Class.query.filter_by(term_id=form.term.data.id, course_id=form.course.data.id).filter(Class.section.ilike(form.section.data)).first()

        if candidate and candidate != class_:
            flash(f'A class with that {wbs.ACADEMIC_TERM.system}, course, and section already exists.')
        else:
            form.populate_obj(class_)
            db.session.commit()
            flash(f'Changes to class #{class_.id} have been made.', 'success')

    return render_template('edit-form.html', title='Classes', card_title=f'Editing Class #{class_.id}: {class_}', form=form)


@classes.route('/<class_id>', methods=['GET', 'POST'])
@login_required
def class_info(class_id):
    current_class = verify_class_exists(class_id)
    students = Student.query.join(Enrollment).filter_by(class_id=class_id)
    return render_template('class-info.html', current_class=current_class, students=students)


@classes.route('/<class_id>/enrollment', methods=['GET', 'POST'])
@admin_required
def enrollment(class_id):
    current_class = verify_user_teaches_class(class_id)
    students = Student.query.join(Enrollment).filter_by(class_id=class_id)
    form = EnrollmentForm()

    if form.validate_on_submit():
        if request.method != 'POST' or not request.form['action']:
            abort(400)

        student = Student.query.filter_by(user_id=form.student.data.user_id).first()

        if student:
            student_enrollment = Enrollment.query.filter_by(student_id=student.user.id, class_id=class_id).first()

            if request.form['action'] == 'Enroll Student':
                if student_enrollment:
                    flash('This student is already enrolled in this class.')
                else:
                    enrollment = Enrollment(student_id=student.user.id, class_id=class_id)
                    db.session.add(enrollment)
                    db.session.commit()
                    flash(f'{student} has been enrolled in this class.', 'success')
            else:
                if student_enrollment:
                    db.session.delete(student_enrollment)
                    db.session.commit()
                    flash(f'{student} has been withdrawn from the class.', 'success')
                else:
                    flash("You cannot withdraw a student that has not been enrolled.")
        else:
            abort(400)

    return render_template('enrollment.html', current_class=current_class, students=students, form=form)


@classes.route('/<class_id>/absence/add/<date>/<student_id>', methods=['POST'])
@admin_required
def mark_absent(class_id, date, student_id):
    utcnow_date = datetime.utcnow().date() if date == 'today' else date
    student_enrollment, student_absence = get_student_info(class_id, student_id, utcnow_date)

    if utcnow_date < student_enrollment.class_.term.start_date:
        flash(f'Date of absence must be on or after the {wbs.ACADEMIC_TERM.system} start date.', 'error')
    elif utcnow_date > student_enrollment.class_.term.end_date:
        flash(f'Date of absence must be on or before the {wbs.ACADEMIC_TERM.system} end date.', 'error')
    else:
        if student_absence:
            flash(f'{student_enrollment.student} has already been marked absent.')
        else:
            absence = Absence(student_id=student_id, class_id=class_id, date=utcnow_date)
            db.session.add(absence)
            db.session.commit()
            flash(f'{student_enrollment.student} has been marked absent.', 'success')

    return redirect(url_for('classes.class_info', class_id=class_id))


@classes.route('/<class_id>/absence/remove/<date>/<student_id>', methods=['POST'])
@admin_required
def remove_absence(class_id, date, student_id):
    if date == 'today':
        student_enrollment, student_absence = get_student_info(class_id, student_id)
    else:
        student_enrollment, student_absence = get_student_info(class_id, student_id, date)

    if student_absence:
        db.session.delete(student_absence)
        db.session.commit()
        flash(f"{student_enrollment.student}'s absence has been removed.", 'success')
    else:
        flash(f"{student_enrollment.student}'s absence has already been removed.")

    if request.referrer:
        return redirect(request.referrer)
    else:
        return redirect(url_for('classes.class_info', class_id=class_id))


@classes.route('/<class_id>/absences/', methods=['GET', 'POST'])
@login_required
def absence_log(class_id):
    current_class = verify_class_exists(class_id)

    if not current_class.has_user(current_user):
        abort(403)

    if current_user.is_teacher:
        absences = Absence.query.filter_by(class_id=class_id).order_by(Absence.date.desc())
    else:
        absences = Absence.query.filter_by(class_id=class_id, student_id=current_user.id).order_by(Absence.date.desc())

    return render_template('absence-log.html', current_class=current_class, absences=absences)


@classes.route('/<class_id>/absences/record', methods=['GET', 'POST'])
@admin_required
def record_absence(class_id):
    current_class = verify_class_exists(class_id)
    absences = Absence.query.filter_by(class_id=class_id).order_by(Absence.date.desc())
    form = AbsenceForm()
    form.student.query = Student.query.join(Enrollment).filter_by(class_id=class_id)

    if form.validate_on_submit():
        # Do not use the template returned by `mark_absent`
        mark_absent(class_id=class_id, date=form.date.data, student_id=form.student.data.user.id)

    return render_template('record-absence.html', current_class=current_class, absences=absences, form=form)
