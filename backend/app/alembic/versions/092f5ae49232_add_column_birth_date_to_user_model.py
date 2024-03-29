"""Add column birth_date to User model

Revision ID: 092f5ae49232
Revises: 36b0b56a95c1
Create Date: 2024-01-11 15:29:33.777761

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '092f5ae49232'
down_revision = '36b0b56a95c1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('birth_date', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'birth_date')
    # ### end Alembic commands ###
