"""add path to user

Revision ID: 25ae6e6945a2
Revises: dee762b76d8e
Create Date: 2022-08-10 23:58:42.875072

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '25ae6e6945a2'
down_revision = 'dee762b76d8e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('path', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'path')
    # ### end Alembic commands ###
