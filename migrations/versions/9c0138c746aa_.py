"""empty message

Revision ID: 9c0138c746aa
Revises: e23cec620241
Create Date: 2019-12-13 18:40:02.349543

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9c0138c746aa'
down_revision = 'e23cec620241'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('AssignmentTypes',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('class_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('weight', sa.Integer(), nullable=False),
    sa.CheckConstraint('weight > 0', name='CC_Weight'),
    sa.ForeignKeyConstraint(['class_id'], ['Classes.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('class_id', 'name')
    )
    op.create_table('Assignments',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('class_id', sa.Integer(), nullable=True),
    sa.Column('assignmenttype_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('weight_numerator', sa.Integer(), nullable=False),
    sa.Column('weight_denominator', sa.Integer(), nullable=False),
    sa.Column('due_date', sa.Date(), nullable=False),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.CheckConstraint('weight_numerator > 0 AND weight_numerator < 101 AND weight_denominator > 0 AND weight_denominator < 101', name='CC_Weight'),
    sa.ForeignKeyConstraint(['assignmenttype_id'], ['AssignmentTypes.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['class_id'], ['Classes.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('class_id', 'assignmenttype_id', 'name')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Assignments')
    op.drop_table('AssignmentTypes')
    # ### end Alembic commands ###
