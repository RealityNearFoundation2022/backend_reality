"""Add cuponredeem table  relations with places

Revision ID: 54043ac81b2d
Revises: a8d6c34cc1ce
Create Date: 2024-01-03 18:38:29.916113

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '54043ac81b2d'
down_revision = 'a8d6c34cc1ce'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('couponreedeemed', sa.Column('place_id', sa.Integer(), nullable=False))
    op.drop_index('ix_couponreedeemed_id', table_name='couponreedeemed')
    op.create_index(op.f('ix_couponreedeemed_id'), 'couponreedeemed', ['id'], unique=False)
    op.drop_index('ix_places_id', table_name='places')
    op.create_index(op.f('ix_places_id'), 'places', ['id'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_places_id'), table_name='places')
    op.create_index('ix_places_id', 'places', ['id'], unique=False)
    op.drop_index(op.f('ix_couponreedeemed_id'), table_name='couponreedeemed')
    op.create_index('ix_couponreedeemed_id', 'couponreedeemed', ['id'], unique=True)
    op.drop_column('couponreedeemed', 'place_id')
    # ### end Alembic commands ###