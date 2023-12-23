"""\<description\>

Revision ID: fb0708977909
Revises: 0ee4571ada0f
Create Date: 2023-10-02 14:44:43.668254

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fb0708977909'
down_revision = '0ee4571ada0f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Medical_records',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('medical_record_number', sa.String(length=255), nullable=False),
    sa.Column('height', sa.Float(), nullable=False),
    sa.Column('weight', sa.Float(), nullable=False),
    sa.Column('cases', sa.String(length=2048), nullable=False),
    sa.Column('medication', sa.String(length=2048), nullable=False),
    sa.Column('notice', sa.String(length=2048), nullable=False),
    sa.Column('hospitalization', sa.Boolean(), nullable=False),
    sa.Column('time', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Ward',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('ward_id', sa.String(length=255), nullable=False),
    sa.Column('bed_number', sa.Integer(), nullable=False),
    sa.Column('medical_record_number', sa.String(length=255), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('time', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Ward')
    op.drop_table('Medical_records')
    # ### end Alembic commands ###