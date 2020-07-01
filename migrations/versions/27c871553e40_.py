"""empty message

Revision ID: 27c871553e40
Revises: 5be8a62e3af8
Create Date: 2020-07-01 17:39:31.982665

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '27c871553e40'
down_revision = '5be8a62e3af8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('event', schema=None) as batch_op:
        batch_op.add_column(sa.Column('ruche', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'ruche', ['ruche'], ['num'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('event', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('ruche')

    # ### end Alembic commands ###
