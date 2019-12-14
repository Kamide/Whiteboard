"""empty message

Revision ID: 50c15042a5d2
Revises: 9c0138c746aa
Create Date: 2019-12-14 14:58:34.892514

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '50c15042a5d2'
down_revision = '9c0138c746aa'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('AssignmentTypes', schema=None) as batch_op:
        batch_op.alter_column('class_id',
               existing_type=sa.INTEGER(),
               nullable=False)

    with op.batch_alter_table('Assignments', schema=None) as batch_op:
        batch_op.alter_column('assignmenttype_id',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.alter_column('class_id',
               existing_type=sa.INTEGER(),
               nullable=False)

    with op.batch_alter_table('Classes', schema=None) as batch_op:
        batch_op.alter_column('course_id',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.alter_column('teacher_id',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.alter_column('term_id',
               existing_type=sa.INTEGER(),
               nullable=False)

    with op.batch_alter_table('Courses', schema=None) as batch_op:
        batch_op.alter_column('department_id',
               existing_type=sa.INTEGER(),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Courses', schema=None) as batch_op:
        batch_op.alter_column('department_id',
               existing_type=sa.INTEGER(),
               nullable=True)

    with op.batch_alter_table('Classes', schema=None) as batch_op:
        batch_op.alter_column('term_id',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.alter_column('teacher_id',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.alter_column('course_id',
               existing_type=sa.INTEGER(),
               nullable=True)

    with op.batch_alter_table('Assignments', schema=None) as batch_op:
        batch_op.alter_column('class_id',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.alter_column('assignmenttype_id',
               existing_type=sa.INTEGER(),
               nullable=True)

    with op.batch_alter_table('AssignmentTypes', schema=None) as batch_op:
        batch_op.alter_column('class_id',
               existing_type=sa.INTEGER(),
               nullable=True)

    # ### end Alembic commands ###
