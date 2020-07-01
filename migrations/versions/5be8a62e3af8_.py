"""empty message

Revision ID: 5be8a62e3af8
Revises: 5dba7149320b
Create Date: 2020-07-01 17:35:58.682437

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5be8a62e3af8'
down_revision = '5dba7149320b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('event', schema=None) as batch_op:
        batch_op.drop_index('ix_event_timestamp')
        batch_op.create_index(batch_op.f('ix_event_timestamp'), ['timestamp'], unique=False)

    with op.batch_alter_table('ruche', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_ruche_age_reine'), ['age_reine'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('ruche', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_ruche_age_reine'))

    with op.batch_alter_table('event', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_event_timestamp'))
        batch_op.create_index('ix_event_timestamp', ['timestamp'], unique=1)

    # ### end Alembic commands ###
