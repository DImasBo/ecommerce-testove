"""added role in user

Revision ID: 61a0c1edd7d8
Revises: aef794d8b308
Create Date: 2022-09-14 08:11:29.060268

"""
from alembic import op
import sqlalchemy as sa
import app


# revision identifiers, used by Alembic.
revision = '61a0c1edd7d8'
down_revision = 'aef794d8b308'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('role', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'role')
    # ### end Alembic commands ###