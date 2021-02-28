"""Add weight column

Revision ID: c7f5cccbc3f0
Revises: 6ae1a6101e45
Create Date: 2021-02-28 16:20:24.873326

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c7f5cccbc3f0'
down_revision = '6ae1a6101e45'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('event', schema=None) as batch_op:
        batch_op.add_column(sa.Column('weight', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('event', schema=None) as batch_op:
        batch_op.drop_column('weight')

    # ### end Alembic commands ###
