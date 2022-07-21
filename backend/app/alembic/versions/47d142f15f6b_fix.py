"""fix

Revision ID: 47d142f15f6b
Revises: e58a952287b7
Create Date: 2022-07-17 19:04:38.014729

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '47d142f15f6b'
down_revision = 'e58a952287b7'
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
               type_=app.models.notification.JsonEncodedDict(),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('notification', 'data',
               existing_type=app.models.notification.JsonEncodedDict(),
               type_=sa.INTEGER(),
               existing_nullable=True)
    op.alter_column('notification', 'type',
               existing_type=sa.String(),
               type_=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###
