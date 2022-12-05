"""add notifications json

Revision ID: 3e12be642267
Revises: b3c51a33d323
Create Date: 2022-06-30 16:41:00.834317

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3e12be642267'
down_revision = '6a90f2eb497c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('notification', 'type',
               existing_type=sa.INTEGER(),
               type_=sa.String(),
               nullable=False)
    op.alter_column('notification', 'data',
               existing_type=sa.INTEGER(),
               type_=sa.String(),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('notification', 'data',
               existing_type=sa.String(),
               type_=sa.INTEGER(),
               existing_nullable=True)
    op.alter_column('notification', 'type',
               existing_type=sa.String(),
               type_=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###
