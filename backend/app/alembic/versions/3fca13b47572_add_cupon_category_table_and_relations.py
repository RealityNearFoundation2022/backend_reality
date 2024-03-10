"""Add cupon category table and relations

Revision ID: 3fca13b47572
Revises: a47b3cee41af
Create Date: 2024-01-03 15:42:38.705316

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3fca13b47572'
down_revision = 'a47b3cee41af'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('couponcategory',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('img', sa.String(), nullable=True),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.Column('created_by', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_by', sa.Integer(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['created_by'], ['user.id'], ),
    sa.ForeignKeyConstraint(['updated_by'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_couponcategory_id'), 'couponcategory', ['id'], unique=False)
    op.add_column('coupon', sa.Column('category_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'coupon', 'couponcategory', ['category_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'coupon', type_='foreignkey')
    op.drop_column('coupon', 'category_id')
    op.drop_index(op.f('ix_couponcategory_id'), table_name='couponcategory')
    op.drop_table('couponcategory')
    # ### end Alembic commands ###