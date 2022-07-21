"""add notifications json

Revision ID: 3ea7a49601d6
Revises: 6f71f461eee1
Create Date: 2022-06-30 17:23:55.678804

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3ea7a49601d6'
down_revision = '6f71f461eee1'
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
               type_=sa.JSON(),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('notification', 'data',
               existing_type=sa.JSON(),
               type_=sa.INTEGER(),
               existing_nullable=True)
    op.alter_column('notification', 'type',
               existing_type=sa.String(),
               type_=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###
