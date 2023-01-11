"""add path2 to asset

Revision ID: 44c809dd0193
Revises: b33e28feb375
Create Date: 2023-01-11 17:36:14.673349

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '44c809dd0193'
down_revision = 'b33e28feb375'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('asset', sa.Column('default', sa.Boolean(), nullable=True))
    op.alter_column('asset', 'path', nullable=True, new_column_name='path_1')
    op.add_column('asset', sa.Column('path_2', sa.String(length=128), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('asset', 'path_2')
    op.alter_column('asset', 'path_1', nullable=True, new_column_name='path')
    op.drop_column('asset', 'default')
    # ### end Alembic commands ###
