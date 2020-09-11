"""empty message

Revision ID: 15251adea781
Revises: 5ecd5f79df40
Create Date: 2020-09-10 16:52:49.568494

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '15251adea781'
down_revision = '5ecd5f79df40'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('event', schema=None) as batch_op:
        batch_op.add_column(sa.Column('rucher', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(batch_op.f('fk_event_rucher_rucher'), 'rucher', ['rucher'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('event', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('fk_event_rucher_rucher'), type_='foreignkey')
        batch_op.drop_column('rucher')

    # ### end Alembic commands ###