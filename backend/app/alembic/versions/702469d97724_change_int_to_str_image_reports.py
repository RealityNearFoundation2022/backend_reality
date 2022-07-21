"""change int to str image reports

Revision ID: 702469d97724
Revises: 9122dd8de0e4
Create Date: 2022-06-29 12:13:05.626611

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '702469d97724'
down_revision = '9122dd8de0e4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('report', 'image',
               existing_type=sa.INTEGER(),
               type_=sa.String(),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('report', 'image',
               existing_type=sa.String(),
               type_=sa.INTEGER(),
               existing_nullable=True)
    # ### end Alembic commands ###
