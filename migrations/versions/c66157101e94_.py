"""empty message

Revision ID: c66157101e94
Revises: 061ed675ef8e
Create Date: 2020-06-16 17:38:18.772084

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c66157101e94'
down_revision = '061ed675ef8e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('ruche', sa.Column('feedback', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('ruche', 'feedback')
    # ### end Alembic commands ###