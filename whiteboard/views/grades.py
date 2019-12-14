from flask import Blueprint, abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required
from whiteboard import settings as wbs
from whiteboard.forms import AssignmentForm, AssignmentTypeForm
from whiteboard.models import Assignment, AssignmentType, db
from whiteboard.views import admin_required
from whiteboard.views.classes import verify_class_exists
from whiteboard.views.exceptions import EntityNotFound

grades = Blueprint('grades', __name__, template_folder='../templates/grades')


# TODO
@grades.route('/grades')
@login_required
def index():
    return render_template('grades.html')


@grades.route('/classes/<class_id>/assignments', methods=['GET', 'POST'])
@login_required
def assignments(class_id):
    current_class = verify_class_exists(class_id)

    if not current_class.has_user(current_user):
        abort(403)

    assignment_types = AssignmentType.query.filter_by(class_id=class_id).order_by(AssignmentType.weight, AssignmentType.name)
    assignments = Assignment.query.filter_by(class_id=class_id).order_by(Assignment.due_date)
    return render_template('assignments.html', current_class=current_class, assignment_types=assignment_types, assignments=assignments)


@grades.route('/classes/<class_id>/assignments-types/new', methods=['GET', 'POST'])
@admin_required
def new_assignment_type(class_id):
    current_class = verify_class_exists(class_id)
    form = AssignmentTypeForm()

    if form.validate_on_submit():
        candidate = AssignmentType.query.filter_by(class_id=class_id).filter(AssignmentType.name.ilike(form.name.data)).first()

        if candidate:
            flash('An assignment type with that name already exists.', 'error')
        else:
            assignment_type = AssignmentType(class_id=class_id)
            form.populate_obj(assignment_type)
            db.session.add(assignment_type)
            db.session.commit()
            flash(f'{assignment_type} has been created.', 'success')
            return redirect(url_for('grades.assignments', class_id=class_id))

    return render_template('edit-form.html', title=current_class, card_title='New Assignment Type (Grading Criteria)', form=form)


@grades.route('/classes/<class_id>/assignments-types/edit/<at_id>', methods=['GET', 'POST'])
@admin_required
def edit_assignment_type(class_id, at_id):
    current_class = verify_class_exists(class_id)
    assignment_types = AssignmentType.query.filter_by(class_id=class_id)
    assignment_type = assignment_types.filter_by(id=at_id).first()

    if not assignment_type:
        raise EntityNotFound(entity_name='Assignment Type (Grading Criteria)', entity_id=at_id)

    form = AssignmentTypeForm(obj=assignment_type)

    if form.validate_on_submit():
        candidate = assignment_types.filter(AssignmentType.name.ilike(form.name.data)).first()

        if candidate and candidate != assignment_type:
            flash('An assignment type (grading criteria) with that name already exists.')
        else:
            form.populate_obj(assignment_type)
            db.session.commit()
            flash(f'Changes to assignment type (grading criteria) #{assignment_type.id} have been made.', 'success')

    return render_template('edit-form.html', title=current_class, card_title=f'Editing Assignment Type (Grading Criteria) #{assignment_type.id}: {assignment_type}', form=form)


@grades.route('/classes/<class_id>/assignments/new', methods=['GET', 'POST'])
@admin_required
def new_assignment(class_id):
    current_class = verify_class_exists(class_id)

    # `len` is used because `current_class.assignment_types` is a Python list
    if len(current_class.assignment_types) < 1:
        flash('Please add an assignment type (grading criteria) first before adding an assignment.')
        return redirect(url_for('grades.assignments', class_id=class_id))

    # Provides assignment name suggestions for teachers
    # `suggestions` is a list of tuples of the form "(id, 'name count+1')"
    suggestions = [(a_t.id, f'{a_t.name} {a_t.count + 1}') for a_t in current_class.assignment_types]
    form = AssignmentForm()
    form.assignmenttype.query = AssignmentType.query.filter_by(class_id=class_id).order_by(AssignmentType.weight, AssignmentType.name)

    if form.validate_on_submit():
        if form.due_date.data < current_class.term.start_date:
            flash(f'Due date must be on or after the {wbs.ACADEMIC_TERM.system} start date.', 'error')
        elif form.due_date.data > current_class.term.end_date:
            flash(f'Due date must be on or before the {wbs.ACADEMIC_TERM.system} end date.', 'error')
        else:
            assignment = Assignment(class_id=class_id)
            form.populate_obj(assignment)
            db.session.add(assignment)
            db.session.commit()
            flash(f'{assignment} has been created.', 'success')
            return redirect(url_for('grades.assignments', class_id=class_id))

    return render_template('edit-assignment.html', title=current_class, card_title='New Assignment', suggestions=suggestions, form=form)


@grades.route('/classes/<class_id>/assignments/edit/<a_id>', methods=['GET', 'POST'])
@admin_required
def edit_assignment(class_id, a_id):
    current_class = verify_class_exists(class_id)

    assignment = Assignment.query.filter_by(class_id=class_id, id=a_id).first()

    if not assignment:
        raise EntityNotFound(entity_name=Assignment.__name__, entity_id=a_id)

    form = AssignmentForm(obj=assignment)
    form.assignmenttype.query = AssignmentType.query.filter_by(class_id=class_id).order_by(AssignmentType.weight, AssignmentType.name)

    if form.validate_on_submit():
        candidate = Assignment.query.filter_by(class_id=class_id).filter(Assignment.name.ilike(form.name.data)).first()

        if candidate and candidate != assignment:
            flash('An assignment with that name already exists.')
        else:
            form.populate_obj(assignment)
            db.session.commit()
            flash(f'Changes to assignment #{assignment.id} have been made.', 'success')

    return render_template('edit-assignment.html', title=current_class, card_title=f'Editing Assignment #{assignment.id}', form=form)
